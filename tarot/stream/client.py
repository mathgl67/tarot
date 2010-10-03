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

from tarot.stream.abstract import AbstractOutputStream, AbstractInputStream, AbstractStream
from tarot.stream.handler.client.other import ErrorHandler, AuthHandler
from tarot.stream.handler.client.game import GameStartHandler, GameDeckHandler
from tarot.stream.handler.client.channel import ChannelJoinHandler, ChannelLeftHandler, ChannelMessageHandler, ChannelUsersHandler

class ClientOutputStream(AbstractOutputStream):
    def admin_shutdown(self):
        self.base("admin-shutdown")
        
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
        
    def game_start(self, user_list):
        self.writer.writeStartElement("game-start")
        for user in user_list:
            self.writer.writeStartElement("user")
            self.writer.writeAttribute("name", user)
            self.writer.writeEndElement()
        self.writer.writeEndElement()
        
class ClientInputStream(AbstractInputStream):
    # define signals
    error_received = QtCore.pyqtSignal(str, str)
    auth_success = QtCore.pyqtSignal()
    auth_error = QtCore.pyqtSignal(int, str)
    channel_join_received = QtCore.pyqtSignal(str)
    channel_left_received = QtCore.pyqtSignal(str)
    channel_users_received = QtCore.pyqtSignal(list)
    channel_message_received = QtCore.pyqtSignal(str, str)
    game_start = QtCore.pyqtSignal(list)
    game_deck = QtCore.pyqtSignal(object)
    
    # define handler class list
    all_handler_class = [
        ErrorHandler, AuthHandler,
        GameStartHandler, GameDeckHandler,
        ChannelJoinHandler, ChannelLeftHandler, ChannelMessageHandler, ChannelUsersHandler
    ]

class ClientStream(AbstractStream):
    def _init_stream(self):
        self.input = ClientInputStream(self)
        self.output = ClientOutputStream(self)
        