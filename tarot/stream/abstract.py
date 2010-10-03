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

from tarot.stream.handler.abstract import StreamHandlerList

from tarot.game.deck import Deck, DeckGeneration

class AbstractOutputStream(QtCore.QObject):
    def __init__(self, stream):
        QtCore.QObject.__init__(self)
        self.stream = stream
        self.writer = QtCore.QXmlStreamWriter(self.stream.socket)

    def start(self):
        self.writer.writeStartDocument()
        self.writer.writeStartElement("stream")
    
    def end(self):
        self.writer.writeEndElement()
        self.writer.writeEndDocument()
        
    def base(self, name, attributes=None):
        self.writer.writeStartElement(name)
        if attributes:
            for attribute, value in attributes.items():
                self.writer.writeAttribute(attribute, value)
        self.writer.writeEndElement()

    def error(self, name, message=None):
        attributes = {"name": name}
        if message:
            attributes["message"] = message
        self.base("error", attributes)

class AbstractInputStream(QtCore.QObject):
    all_handler_class=None
    
    def __init__(self, stream):
        QtCore.QObject.__init__(self)
        self.stream = stream
        self.reader = QtCore.QXmlStreamReader()
        
        self.handler_list = StreamHandlerList(self.stream)
        self.handler_list.from_class_list(self.all_handler_class)
        
        self.stream.socket.readyRead.connect(self.ready_read)
    
    def parse_attributes(self):
        attr_list = self.reader.attributes()
        attributes = {}
        for idx in range(0, attr_list.size()):
            attr = attr_list.at(idx)
            attributes[str(attr.name().toString())] = str(attr.value().toString())
            
        return attributes
    
    def parse_user_list(self):
        user_list = []
        while not self.reader.atEnd():
            self.reader.readNext()
            if self.reader.isEndElement():
                if "user" != self.reader.name().toString():
                    break
            elif self.reader.isStartElement():
                if "user" == self.reader.name().toString():
                    attributes = self.parse_attributes()
                    user_list.append(attributes["name"])
        return user_list
    
    def parse_card(self):
        attributes = self.parse_attributes()
        if attributes.has_key("id"):
            full = DeckGeneration.full()
            for card in full.card_list:
                if card.id() == attributes["id"]:
                    return card
        return None
        
    def parse_deck(self):
        deck = Deck()
        while not self.reader.atEnd():
            self.reader.readNext()
            if self.reader.isEndElement():
                if "card" != self.reader.name().toString():
                    break
            elif self.reader.isStartElement():
                if "card" == self.reader.name().toString():
                    card = self.parse_card()
                    if card:
                        deck.append(card)
        return deck
    
    def handle(self, name):
        self.handler_list.run(name)
    
    def ready_read(self):
        content = self.stream.socket.readAll()
        print "content:", content
        self.reader.addData(content)
        
        while not self.reader.atEnd():
            self.reader.readNext()
            if self.reader.hasError():
                if self.reader.error() == QtCore.QXmlStreamReader.PrematureEndOfDocumentError:
                    print "document not finish.."
                    return
                else:
                    print "document error:", self.reader.errorString()
                    print "closing socket"
                    self.stream.socket.close()
            else:
                if self.reader.isEndDocument():
                    print "document end: closing socket"
                    self.stream.socket.close()
                elif self.reader.isStartElement():
                    print "document element start"
                    if self.reader.name().toString() != "stream":
                        self.handle(self.reader.name().toString())
                    

class AbstractStream(QtCore.QObject):
    def __init__(self, socket, context=None):
        QtCore.QObject.__init__(self)
        self.socket = socket
        self.context = context
        self.input = None
        self.output = None
        self._init_stream()
        
    def _init_stream(self):
        pass
