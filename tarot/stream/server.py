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
from tarot.stream.handler.server.admin import AdminShutdownStreamHandler
from tarot.stream.handler.server.channel import ChannelEnterStreamHandler, ChannelUsersStreamHandler, ChannelMessageStreamHandler
from tarot.stream.handler.server.game import GameStartStreamHandler
from tarot.stream.handler.server.other import ErrorStreamHandler, AuthStreamHandler

from tarot.game.card import Card, FaceCard, TrumpCard, ExcuseCard 

class ServerOutputStream(AbstractOutputStream):
    def game_start(self, user_list):
        self.writer.writeStartElement("game-start")
        for user in user_list:
            self.writer.writeStartElement("user")
            self.writer.writeAttribute("name", user)
            self.writer.writeEndElement()
        self.writer.writeEndElement()
    
    def game_card(self, card):
        self.writer.writeStartElement("card")
        self.writer.writeAttribute("id", card.id())    
        self.writer.writeEndElement()
    
    def game_deck(self, deck):
        self.writer.writeStartElement("game-deck")
        
        for card in deck.card_list:
            self.game_card(card)
                    
        self.writer.writeEndElement()
        
class ServerChannelOutputStream(QtCore.QObject):
    def __init__(self, stream):
        QtCore.QObject.__init__(self)
        self.stream = stream
        self.session = stream.context
        self.server = self.session.server
    
    def base(self, name, attributes=None):
        for session in self.server.session_list.get_by_channel(self.stream.context.channel):
            session.stream.output.base(name, attributes)

    def game_start(self, user_list):
        for session in self.server.session_list.get_by_channel(self.stream.context.channel):
            session.stream.output.game_start(user_list)

class ServerInputStream(AbstractInputStream):
    all_handler_class = [
        AdminShutdownStreamHandler,
        ChannelEnterStreamHandler, ChannelUsersStreamHandler, ChannelMessageStreamHandler,
        GameStartStreamHandler,
        ErrorStreamHandler, AuthStreamHandler
    ]

class ServerStream(AbstractStream):
    def _init_stream(self):
        self.input = ServerInputStream(self)
        self.output = ServerOutputStream(self)
        self.output_channel = ServerChannelOutputStream(self)
        