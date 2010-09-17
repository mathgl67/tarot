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

from tarot.game.deck import DeckGeneration
from tarot.game.distribute import Distribute
from tarot.game.player import PlayerList

from PyQt4 import QtCore

class Game(QtCore.QObject):
    def __init__(self):
        super(Game, self).__init__()
        self.player_list = PlayerList()
        self.contract = None
        self.deck = DeckGeneration.full()
        self.deck.shuffle()
        self.dog = None
    
    def distribute(self):
        distribute = Distribute(self.deck, self.player_list.player_count)
        (player_deck_list, self.dog) = distribute.do()
        
        self.player_list.nextDistributer()
        print self.player_list.distributer
        player_first = self.player_list.getPlayerAfter(self.player_list.distributer)
        self.player_list.reorder(player_first)
        
        index = 0
        for player in self.player_list.next():
            print player
            player.hand = player_deck_list[index]
            index += 1
    