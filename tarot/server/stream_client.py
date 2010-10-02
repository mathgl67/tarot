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
from tarot.server.stream import AbstractOutputStream, AbstractInputStream, AbstractStream

class ClientOutputStream(AbstractOutputStream):
    def auth(self, username, password):
        self.base("auth", {"user": username, "password": password})

    def channel_enter(self, name, password):
        self.base("channel-enter", {"name": name, "password": password})

    def channel_leave(self, username):
        self.base("channel-leave", {"user": username})
        
    def channel_message(self, message):
        self.base("channel-message", {"message": message})

    def channel_users(self):
        self.base("channel-users")

class ClientInputStream(AbstractInputStream):
    channel_join_received = QtCore.pyqtSignal(str)
    channel_left_received = QtCore.pyqtSignal(str)
    channel_users_received = QtCore.pyqtSignal(list)
    channel_message_received = QtCore.pyqtSignal(str, str)
    
    def parse_attributes(self):
        attr_list = self.reader.attributes()
        attributes = {}
        for idx in range(0, attr_list.size()):
            attr = attr_list.at(idx)
            attributes[str(attr.name().toString())] = str(attr.value().toString())
        
        return attributes
    
    def handle(self, name):
        print "handle command name:", name
        if "channel-message" == name:
            attributes = self.parse_attributes()
            self.channel_message_received.emit(attributes["user"], attributes["message"])
        elif "channel-join" == name:
            attributes = self.parse_attributes()
            self.channel_join_received.emit(attributes["user"])
        elif "channel-left" == name:
            attributes = self.parse_attributes()
            self.channel_left_received.emit(attributes["user"])
        elif "channel-users" == name:
            user_list = []
            while not self.reader.atEnd():
                self.reader.readNext()
                if self.reader.isEndElement():
                    if "channel-users" == self.reader.name().toString():
                        break
                elif self.reader.isStartElement():
                    if "user" == self.reader.name().toString():
                        attributes = self.parse_attributes()
                        user_list.append(attributes["name"])
            
            self.channel_users_received.emit(user_list)

class ClientStream(AbstractStream):
    def _init_stream(self):
        self.input = ClientInputStream(self)
        self.output = ClientOutputStream(self)
        