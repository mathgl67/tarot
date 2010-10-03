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


from tarot.stream.handler.server.abstract import AbstractServerStreamHandler


class ChannelEnterStreamHandler(AbstractServerStreamHandler):
    name="channel-enter"
    
    def run(self):
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
        name = self.attributes.get("name", None)
        password = self.attributes.get("password", None)
        
        channel = self.server.config_store.channel_list.get_by_name(name)
        if channel:
            if channel.verify_password(password):
                print "user %s enter in channel %s" % (self.session.user.name, channel.name)
                self.session.channel = channel
                # inform people in channel
                self.output_channel.base("channel-join", {"user": self.session.user.name})
                # set success
                self.output.base("channel-enter", {"result": "success"})
            else:
                print "user %s bad password for channel %s" % (self.session.user.name, channel.name)
                self.output.base("channel-enter", {
                    "result": "error",
                    "code": "2",
                    "message": "Wrong password" 
                })
            return
        else:
                print "user %s want enter in channel %s that not exists" % (self.session.user.name, name)
                self.output.base("channel-enter", {
                    "result": "error",
                    "code": "1",
                    "message": "Channel does'nt exists."
                })
                

class ChannelUsersStreamHandler(AbstractServerStreamHandler):
    name="channel-users"
    
    def run(self):
        """
            <channel-users />
            
            return:
                <channel-users>
                    <user name="user1" />
                    <user name="user2" />
                </channel-users>
        """
        print "user %s ask for user list in chan %s" % (self.session.user.name, self.session.channel.name)
        session_list = self.server.session_list.get_by_channel(self.session.channel)
        self.output.writer.writeStartElement("channel-users")
        for session in session_list:
            self.output.writer.writeStartElement("user")
            self.output.writer.writeAttribute("name", session.user.name)
            self.output.writer.writeEndElement()
        self.output.writer.writeEndElement()


class ChannelMessageStreamHandler(AbstractServerStreamHandler):
    name="channel-message"
    
    def run(self):
        """
            <channel-message message="a message" />
                    
            channel event:
                <channel-message user="user1" message="a message" />
        """
        print "user %s send message to %s" % (self.session.user.name, self.session.channel.name)
        message = self.attributes.get("message", "")
        
        self.output_channel.base("channel-message", {"user": self.session.user.name, "message": message})


_module_handler_list = [ChannelEnterStreamHandler, ChannelMessageStreamHandler, ChannelUsersStreamHandler]