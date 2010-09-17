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

class PlayerList(QtCore.QObject):
    def __init__(self):
        self.player_list = []
        self.player_count = 0
        self.distributer = None
        
    def append(self, player):
        # define id and order to sort the list
        player.order = self.player_count
        # increment player_count to have a length cache
        self.player_count += 1
        # finally append to list
        self.player_list.append(player)
    
    def __repr__(self):
        player_str = []
        for player in self.player_list:
            player_str.append(repr(player))
        return "PlayerList(%s)" % (",".join(player_str))
    
    def next(self):
        for player in self.player_list:
            yield player
    
    def reorder(self, player_first):
        adjustement = self.player_count - player_first.order
        for player in self.player_list:           
            player.order = (player.order + adjustement) % self.player_count
        self.player_list = sorted(self.player_list, key=lambda p: p.order)        

    def getPlayerAfter(self, player):
        next_order = (player.order + 1) % self.player_count
        for p in self.next():
                if p.order == next_order:
                    return p
        return None
    
    def nextDistributer(self):
        if not self.distributer:
            # this should not append and first distributer should be
            # handle by another way
            self.distributer = self.player_list[0]
        else:
            self.distributer = self.getPlayerAfter(self.distributer)
    
class Player(QtCore.QObject):
    
    takeList = { "pass": 0, "little": 1, "guard": 2, "guard against": 3, "guard without": 4 }
    
    def __init__(self, user):
        super(Player,self).__init__()
        self.id = 0
        self.user = user
        self.order = 0
        self.score = 0
        self.hand = None
    
    def __repr__(self):
        return "Player(%s)" % self.user.name
