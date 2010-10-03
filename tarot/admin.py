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
from ConfigParser import ConfigParser

from tarot.stream.client import ClientStream

class AdminApplication(QtCore.QCoreApplication):
    def __init__(self, argv):
        QtCore.QCoreApplication.__init__(self, argv)
        
        self.config = ConfigParser()
        self.config.read("config/admin.ini")
        
        self.socket = QtNetwork.QTcpSocket()
        self.stream = ClientStream(self.socket)
        
        self.stream.input.auth_success.connect(self.auth_success)
        
        self.socket.error.connect(self.socket_error)
        self.socket.connected.connect(self.socket_connected)
        self.socket.disconnected.connect(self.socket_disconnected)
        self.socket_connect()
        
    def socket_connect(self):
        hostname = self.config.get("admin", "hostname")
        port = self.config.getint("admin", "port")
        self.socket.connectToHost(hostname, port)
        
    def socket_connected(self):
        self.stream.output.start()
        username = self.config.get("admin", "username")
        password = self.config.get("admin", "password")
        self.stream.output.auth(username, password)
    
    def socket_error(self, error):
        if error == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            print "ERROR: connection refused!"
        self.quit()        
    
    def socket_disconnected(self):
        self.quit()    
    
    def auth_success(self):
        command_name = self.argv()[1]
        if command_name == "shutdown":
            self.stream.output.admin_shutdown()
        else:
            print "ERROR: command not found."    
        self.socket.close()
        
        
        
        