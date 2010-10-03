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

from tarot.stream.handler.abstract import AbstractStreamHandler


class ChannelJoinHandler(AbstractStreamHandler):
    name="channel-join"
    
    def run(self):
        self.input.channel_join_received.emit(self.attributes["user"])


class ChannelMessageHandler(AbstractStreamHandler):
    name="channel-message"
    
    def run(self):
        self.input.channel_message_received.emit(self.attributes["user"], self.attributes["message"])


class ChannelLeftHandler(AbstractStreamHandler):
    name="channel-left"
    
    def run(self):
        self.input.channel_left_received.emit(self.attributes["user"])


class ChannelUsersHandler(AbstractStreamHandler):
    name="channel-users"
    
    def parse(self):
        self.user_list = []
        while not self.input.reader.atEnd():
            self.input.reader.readNext()
            if self.input.reader.isEndElement():
                if "channel-users" == self.input.reader.name().toString():
                    break
            elif self.input.reader.isStartElement():
                if "user" == self.input.reader.name().toString():
                    attributes = self.input.parse_attributes()
                    self.user_list.append(attributes["name"])

    def run(self):
        self.input.channel_users_received.emit(self.user_list)
        

_module_handler_list = [ChannelJoinHandler, ChannelLeftHandler, ChannelMessageHandler, ChannelUsersHandler]
