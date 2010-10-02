#
# -*- coding: utf8 -*-
#
# Tarot 
# Copyright (C) 2009-2010  mathgl67@gmail.com
#
#  This file is part of Tarot
#
#  Tarot is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Tarot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Tarot.  If not, see <http://www.gnu.org/licenses/>.
#

from PyQt4 import QtCore

from tarot.server.game import Game

class AbstractCommand(QtCore.QObject):
    name=None
    must_be_auth=True
    must_be_admin=False
    
    @staticmethod
    def run(stream):
        pass
    
class CommandList(list):
    def __init__(self):
        list.__init__(self)
        self._init_commands()
  
    def _init_commands(self):
        self.append(AdminShutdownCommand)
        self.append(AuthCommand)
        self.append(ChannelEnterCommand)
        self.append(ChannelUsersCommand)
        self.append(ChannelMessageCommand)
        self.append(GameStartCommand)
  
    def get_by_name(self, name):
        for command in self:
            if command.name == name:
                return command
        return None
  
    def run(self, name, stream):
        command = self.get_by_name(name)
        session = stream.context
        if command:        
            if command.must_be_auth and not session.user:
                stream.output.error("command_not_allowed")
                return
            
            if command.must_be_admin and session.user and not session.user.is_admin:
                stream.output.error("command_not_allowed")
                return
                                
            command.run(stream)
        else:
            print "command unknown:", name
            stream.output.error("command_unknown")
            return

class AdminShutdownCommand(AbstractCommand):
    name="admin-shutdown"
    must_be_admin=True
    
    @staticmethod
    def run(stream):
        """
            <admin-shutdown />

        """
        stream.context.server.application.quit()
        

class AuthCommand(AbstractCommand):
    name="auth"
    must_be_auth=False
    
    @staticmethod
    def run(stream):
        """
            <auth user="name" password="password" />
            
            return:
                * <auth result="success" />
                * <auth result="error" code="1" message="An error message" />
            
            code/message:
                1 - User or password incorrect
                2 - User already have a session
        """
        session = stream.context
        attributes = stream.input.parse_attributes()
        user_name = attributes.get("user", None)
        user = session.server.config_store.user_list.get_by_name(user_name)
        if user:
            print "user found"
            if user.verify_password(attributes["password"]):
                print "user password okay"
                if not session.server.session_list.user_exists(user):
                    print "user %s authentified" % (user.name)
                    session.user = user
                    stream.output.base("auth", { "result": "success" })
                    return
                else:
                    print "user %s already have a session" % (user.name)
                    stream.output.base("auth", {
                        "result": "error",
                        "code": "2",
                        "message": "User already have a session."
                    })
                    return
        
        print "bad authententification"
        stream.output.base("auth", {
            "result": "error",
            "code": "1",
            "message": "User or password incorrect"
        })
        
class ChannelEnterCommand(AbstractCommand):
    name="channel-enter"
    
    @staticmethod
    def run(stream):
        """
            <channel-enter name="chan1" password="pass" />
            
            return:
                <channel-enter result="success" />
                <channel-enter result="error" code="1" message="an error message" />
            
            channel event:
                <channel-join user="name" />
            
            code / message:
                1 - Channel doesn't exists.
                2 - Channel bad password.
        """
        session = stream.context
        attributes = stream.input.parse_attributes()        
        name = attributes.get("name", None)
        password = attributes.get("password", None)
        
        channel = session.server.config_store.channel_list.get_by_name(name)
        if channel:
            if channel.verify_password(password):
                print "user %s enter in channel %s" % (session.user.name, channel.name)
                session.channel = channel
                # inform people in channel
                stream.output_channel.base("channel-join", {"user": session.user.name})
                # set success
                stream.output.base("channel-enter", {"result": "success"})
            else:
                print "user %s bad password for channel %s" % (session.user.name, channel.name)
                stream.output.base("channel-enter", {
                    "result": "error",
                    "code": "2",
                    "message": "Wrong password" 
                })
            return
        else:
                print "user %s want enter in channel %s that not exists" % (session.user.name, name)
                stream.output.base("channel-enter", {
                    "result": "error",
                    "code": "1",
                    "message": "Channel does'nt exists."
                })
                

class ChannelUsersCommand(AbstractCommand):
    name="channel-users"
    
    @staticmethod
    def run(stream):
        """
            <channel-users />
            
            return:
                <channel-users>
                    <user name="user1" />
                    <user name="user2" />
                </channel-users>
        """
        print "user %s ask for user list in chan %s" % (stream.context.user.name, stream.context.channel.name)
        session_list = stream.context.server.session_list.get_by_channel(stream.context.channel)
        stream.output.writer.writeStartElement("channel-users")
        for session in session_list:
            stream.output.writer.writeStartElement("user")
            stream.output.writer.writeAttribute("name", session.user.name)
            stream.output.writer.writeEndElement()
        stream.output.writer.writeEndElement()

class ChannelMessageCommand(AbstractCommand):
    name="channel-message"
    
    @staticmethod
    def run(stream):
        """
            <channel-message message="a message" />
                    
            channel event:
                <channel-message user="user1" message="a message" />
        """
        session = stream.context
        print "user %s send message to %s" % (session.user.name, session.channel.name)
        attributes = stream.input.parse_attributes()
        message = attributes.get("message", "")
        
        stream.output_channel.base("channel-message", {"user": session.user.name, "message": message})

class GameStartCommand(AbstractCommand):
    name="game-start"    
    
    @staticmethod
    def run(stream):
        """
            <game-start>user_list</game-start>
            
            user_list:
                <user name="user1" />
            
            return:
                <game-start-error name="invalid_user_count" />
                
            user event:
                <game-deck />
                <game-contract />

            channel event:
                <game-started />
            
        """
        session = stream.context
        print "user %s start game in channel %s" % (session.user.name, session.channel.name)
        game = Game()
        
        child = element.firstChildElement() # yes not adapted..
        while not child.isNull():
            if child.tagName() == "user":
                game.append_player_session(
                    session.server.session_list.get_by_user_name(child.attribute("name"))
                )              
            child = child.nextSiblingElement()
        
        # player count check
        if not game.have_valid_player_count():
            print "game_start: invalid user count."
            session.send_line(
                Message.simple("game-start-error", {"name": "invalid_user_count"})
            )
            return
        
        # distribute
        game.distribute()
        