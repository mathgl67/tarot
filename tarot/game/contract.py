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

class Contract(QtCore.QObject):
    
    finished=QtCore.pyqtSignal()
    updated=QtCore.pyqtSignal()
    
    def __init__(self, player_list):
        super(Contract, self).__init__()
        self.player_list = player_list
        self.contract = {}
        self.currentPlayer = None
    
    def askPlayer(self, player):
        print "ask to player:", player
        self.currentPlayer = player
        player.takeDecided.connect(self.takeDecided)
        player.take(self.contract)
        
    def run(self):
        print "run contract"
        #asking to the first player
        self.askPlayer(self.player_list.player_list[0])
            
    def takeDecided(self, value):
        print "decided:", value
        self.contract[self.currentPlayer.id] = value
        self.updated.emit()
        #ask next player
        nextPlayer = self.player_list.getPlayerAfter(self.currentPlayer)
        if not self.contract.has_key(nextPlayer.id):
            self.askPlayer(nextPlayer)
        else:
            self.finished.emit()
    
    def whoOwn(self):
        best_offer = 0
        best_offer_id = None
        
        for id, value in self.contract.iteritems():
            print "o:", (id,value)
            if value > best_offer:
                best_offer = value
                best_offer_id = id
                
        if best_offer_id != None:
            for player in self.player_list.next():
                if player.id == best_offer_id:
                    return player
        return None