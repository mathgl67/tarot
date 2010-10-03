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

from PyQt4 import QtCore, QtGui

class UsersWidget(QtCore.QObject):
    def __init__(self, window):
        QtCore.QObject.__init__(self)
    
        self.window = window
        self.user_list = self.window.ui.listWidgetUsers
        self.stream = window.stream     
        
        self.game_players = []
        
        self.window.ui.pushButtonSetUnsetPlayer.clicked.connect(self.set_unset_player)
        self.window.ui.pushButtonStartGame.clicked.connect(self.start_game)
    
        self.stream.input.channel_users_received.connect(self.set_user_list)
        
    def set_user_list(self, user_list):
        self.user_list.clear()
        for user in user_list:
            self.user_list.addItem(user)
    
    def set_unset_player(self):
        selected = self.user_list.selectedItems()
        for sel in selected:
            user_name = sel.text()
            
            if user_name not in self.game_players:
                print "select:", user_name
                sel.setBackgroundColor(QtGui.QColor("green"))
                self.game_players.append(user_name)
                sel.setSelected(False)
            else:
                print "unselect:", user_name
                sel.setBackgroundColor(QtGui.QColor("white"))
                self.game_players.remove(user_name)
                sel.setSelected(False)
    
    def start_game(self):
        self.stream.output.game_start(self.game_players)
    