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

from tarot.server.session import SessionList, Session

from PyQt4 import QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, application, config_store):
        QtNetwork.QTcpServer.__init__(self)
        self.application = application
        self.newConnection.connect(self.new_connection)
        
        self.config_store = config_store
        self.session_list = SessionList()
            
    def listen(self):
        if self.config_store.listen_host:
            host = QtNetwork.QHostAddress()
            host.setAddress(self.config_store.listen_host)
        else:
            host = QtNetwork.QHostAddress.Any
        
        return QtNetwork.QTcpServer.listen(
            self,
            host, #(self.config_store.host),
            self.config_store.listen_port
        )
    
    def new_connection(self):
        print "new connection: add to session list"
        client = self.nextPendingConnection()
        session = Session(self, client)
        session.start()
