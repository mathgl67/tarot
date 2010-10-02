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

from tarot.server.message import Message
from tarot.server.game import Game

class AbstractCommand(QtCore.QObject):
    name=None
    must_be_auth=True
    must_be_admin=False
    
    @staticmethod
    def parse_attributes(session):
        attr_list = session.reader.attributes()
        attributes = {}
        for idx in range(0, attr_list.size()):
            attr = attr_list.at(idx)
            attributes[str(attr.name().toString())] = str(attr.value().toString())
        
        return attributes
    
    @staticmethod
    def run(session):
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
  
    def run(self, name, session):
        command = self.get_by_name(name)
        if command:        
            if command.must_be_auth and not session.user:
                session.socket.write("<command-not-allowed />\n")
                return
            
            if command.must_be_admin and session.user and not session.user.is_admin:
                session.socket.write("<command-not-allowed />\n")
                return
                                
            command.run(session)
        else:
            print "command unknown:", name
            session.socket.write("<command-unknown />\n")
            return

class AdminShutdownCommand(AbstractCommand):
    name="admin-shutdown"
    must_be_admin=True
    
    @staticmethod
    def run(session):
        """
            <admin-shutdown />

        """
        session.server.application.quit()
        

class AuthCommand(AbstractCommand):
    name="auth"
    must_be_auth=False
    
    @staticmethod
    def run(session):
        """
            <auth user="name" password="password" />
            
            return:
                * <auth result="success" />
                * <auth result="error" code="1" message="An error message" />
            
            code/message:
                1 - User or password incorrect
                2 - User already have a session
        """
        attributes = AuthCommand.parse_attributes(session)
        user_name = attributes.get("user", None)
        user = session.server.config_store.user_list.get_by_name(user_name)
        if user:
            print "user found"
            if user.verify_password(attributes["password"]):
                print "user password okay"
                if not session.server.session_list.user_exists(user):
                    print "user %s authentified" % (user.name)
                    session.user = user
                    session.send_line(Message.simple("auth", { "result": "success" }))
                    return
                else:
                    print "user %s already have a session" % (user.name)
                    session.send_line(Message.simple("auth", {
                        "result": "error",
                        "code": "2",
                        "message": "User already have a session."
                    }))
                    return
        
        print "bad authententification"
        session.send_line(Message.simple("auth", {
            "result": "error",
            "code": "1",
            "message": "User or password incorrect"
        }))
        
class ChannelEnterCommand(AbstractCommand):
    name="channel-enter"
    
    @staticmethod
    def run(session):
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
        attributes = ChannelEnterCommand.parse_attributes(session)        
        name = attributes.get("name", None)
        password = attributes.get("password", None)
        
        channel = session.server.config_store.channel_list.get_by_name(name)
        if channel:
            if channel.verify_password(password):
                print "user %s enter in channel %s" % (session.user.name, channel.name)
                session.channel = channel
                # inform people in channel
                session.server.session_list.send_to_channel(
                    session.channel,
                    Message.simple("channel-join", {"user": session.user.name})
                )
                # set success
                session.send_line(Message.simple("channel-enter", {"result": "success"}))
            else:
                print "user %s bad password for channel %s" % (session.user.name, channel.name)
                session.send_line(Message.simple("channel-enter", {
                    "result": "error",
                    "code": "2",
                    "message": "Wrong password"
                }))
            return
        else:
                print "user %s want enter in channel %s that not exists" % (session.user.name, name)
                session.send_line(Message.simple("channel-enter", {
                    "result": "error",
                    "code": "1",
                    "message": "Channel does'nt exists."
                }))
                

class ChannelUsersCommand(AbstractCommand):
    name="channel-users"
    
    @staticmethod
    def run(session):
        """
            <channel-users />
            
            return:
                <channel-users>
                    <user name="user1" />
                    <user name="user2" />
                </channel-users>
        """
        print "user %s ask for user list in chan %s" % (session.user.name, session.channel.name)
        session_list = session.server.session_list.get_by_channel(session.channel)
        session.send_line(Message.channel_users(session_list))

class ChannelMessageCommand(AbstractCommand):
    name="channel-message"
    
    @staticmethod
    def run(session):
        """
            <channel-message message="a message" />
                    
            channel event:
                <channel-message user="user1" message="a message" />
        """
        print "user %s send message to %s" % (session.user.name, session.channel.name)
        attributes = ChannelMessageCommand.parse_attributes(session)
        message = attributes.get("message", "")
        
        session.server.session_list.send_to_channel(
            session.channel,
            Message.simple("channel-message", {"user": session.user.name, "message": message})
        )

class GameStartCommand(AbstractCommand):
    name="game-start"    
    
    @staticmethod
    def run(session):
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
        