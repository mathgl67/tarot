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

from PyQt4 import QtGui, QtNetwork

from tarot.ui.widget.chat import ChatWidget
from tarot.ui.generated.game import Ui_GameWindow
from tarot.ui.window.new_connection import ConnectionDialog
from tarot.server.stream_client import ClientStream


class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connected.connect(self.connected)
        
        self.stream = ClientStream(self.socket)
        self.stream.input.stream_initialized.connect(self.stream_initialized)
        self.stream.input.channel_message_received.connect(self.channel_message_received)
        self.stream.input.channel_join_received.connect(self.channel_join_received)
        self.stream.input.channel_left_received.connect(self.channel_left_received)
        self.stream.input.channel_users_received.connect(self.channel_users_received)
        
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
 
        self.ui.actionConnection.triggered.connect(self.connection)
        self.chat_widget = ChatWidget(self)
        
        #game tab
        self.ui.pushButtonAppendGame.clicked.connect(self.append_to_game)
        self.ui.pushButtonGameStart.clicked.connect(self.game_start)
                 
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
            self.stream.output.start()
    
    def stream_initialized(self):
            print "stream initialized"
            self.stream.output.auth(
                self.connection_opts["user"],
                self.connection_opts["user_password"]
            )
            self.stream.output.channel_enter(
                self.connection_opts["channel"],
                self.connection_opts["channel_password"]
            )

    def append_to_game(self):
        selected = self.ui.listWidgetUsers.selectedItems()
        if len(selected) == 1:
            user = selected[0].text()
            self.ui.listWidgetPlayers.addItem(user)

    def game_start(self):
        player_count = self.ui.listWidgetPlayers.count()
        #if not player_count >= 3 or not player_count <= 5:
        #    message = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Error", "You can start game only if you have between 3 and 5 players")
        #    message.exec_()
        
        user_list = []      
        for item_index in range(0, player_count): 
            item = self.ui.listWidgetPlayers.item(item_index)
            user_list.append(item.text())
        
        self.socket.game_start(user_list)

    def channel_join_received(self, user):
        self.chat_widget.notice("%s enter." % user)
        print "ask channel users update"
        self.stream.output.channel_users()

    def channel_left_received(self, user):
        self.chat_widget.notice("%s left." % user)
        print "ask channel users update"
        self.stream.output.channel_users()

    def channel_message_received(self, user, message):
        self.chat_widget.message(user, message) 
    
    def channel_users_received(self, user_list):
        self.ui.listWidgetUsers.clear()
        for user in user_list:
            self.ui.listWidgetUsers.addItem(user)
