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

from PyQt4 import QtCore, QtNetwork
from tarot.server.message import Message

class Client(QtNetwork.QTcpSocket):
    channel_join_received = QtCore.pyqtSignal(str)
    channel_left_received = QtCore.pyqtSignal(str)
    channel_users_received = QtCore.pyqtSignal(list)
    channel_message_received = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        QtNetwork.QTcpSocket.__init__(self)
        self.readyRead.connect(self.ready_read)
        self.reader = QtCore.QXmlStreamReader()
        
    def send_line(self, line):
        self.write("%s\n" % line)
    
    def stream(self):
        self.send_line("<stream>") 
        
    def auth(self, user, password):
        self.send_line(Message.simple("auth", {
           "user": user,
           "password": password 
        }))
        
    def channel_enter(self, name, password):
        self.send_line(Message.simple("channel-enter", {
            "name": name,
            "password": password
        }))
        
    def channel_message(self, message):
        self.send_line(Message.simple("channel-message", {
            "message": message
        }))
    
    def channel_users(self):    
        self.send_line(Message.simple("channel-users"))
    
    def game_start(self, user_list):
        self.send_line(Message.game_start(user_list))
    
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
    
    def ready_read(self):
        content = self.readAll()
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
                    self.reader.clear()
            else:
                if self.reader.isStartDocument():
                    print "document start"
                    continue
                elif self.reader.isEndDocument():
                    print "document end: closing socket"
                    self.close()
                elif self.reader.isEndElement():
                    print "document element ended..."
                elif self.reader.isStartElement():
                    print "document element start"
                    if not self.reader.name().toString() == "stream":
                        self.handle(self.reader.name().toString())
