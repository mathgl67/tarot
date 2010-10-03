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

import os

from PyQt4 import QtGui, QtNetwork

from tarot.ui.widget.chat import ChatWidget
from tarot.ui.widget.users import UsersWidget
from tarot.ui.widget.hand import HandWidget

from tarot.ui.generated.game import Ui_GameWindow
from tarot.ui.window.new_connection import ConnectionDialog
from tarot.ui.image.store import ImageStore

from tarot.stream.client import ClientStream


class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.image_store = ImageStore(os.path.join("images", "cards"))
        
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connected.connect(self.connected)
        
        self.stream = ClientStream(self.socket)    
        
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.ui.actionConnection.triggered.connect(self.connection)
        
        self.chat_widget = ChatWidget(self)
        self.user_widget = UsersWidget(self)
        self.hand_widget = HandWidget(self)
                 
    def connection(self):
        dialog = ConnectionDialog()
        if dialog.exec_():
            print "get connection option"
            self.connection_opts = dialog.get_result()
            print "options:", repr(self.connection_opts)
            print "connect"
            self.socket.connectToHost(
                self.connection_opts["host"],
                self.connection_opts["port"]
            )
    
    def connected(self):
            print "connected"
            self.stream.output.start()
            self.stream.output.auth(
                self.connection_opts["user"],
                self.connection_opts["user_password"]
            )
            self.stream.output.channel_enter(
                self.connection_opts["channel"],
                self.connection_opts["channel_password"]
            )
    
         
    