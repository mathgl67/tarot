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

from tarot.stream.client import ClientStream

class Bot(QtCore.QObject):
    
    quitRequested=QtCore.pyqtSignal()
    
    def __init__(self, options):
        QtCore.QObject.__init__(self)
        
        self.options = options
        
        self.socket  = QtNetwork.QTcpSocket()
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.stream = ClientStream(self.socket)
        self.stream.input.channel_message_received.connect(self.channel_message_received)
    
    def connectToHost(self, host, port):    
        self.socket.connectToHost(host, port)
        
    def connected(self):
        self.stream.output.start()
        self.stream.output.auth(self.options["user"], self.options["user_password"])
        self.stream.output.channel_enter(self.options["channel"], self.options["channel_password"])
    
    def disconnected(self):
        self.quitRequested.emit()
    
    def channel_message_received(self, user, message):
        if message == "quit":
            self.quitRequested.emit()
