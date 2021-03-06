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

from PyQt4 import QtCore

class Game(QtCore.QObject):
    def __init__(self, user_list):
        QtCore.QObject.__init__(self)
        self.player_list = user_list
        self.deck = {}
        self.contract = {}
        self.dog = None
    
    def distribute(self):
        full = DeckGeneration.full()
        full.shuffle()
        
        distributer = Distribute(full, len(self.player_list))
        (deck_list, self.dog) = distributer.do()
        idx = 0
        for player in self.player_list:
            self.deck[player] = deck_list[idx]
            idx=idx+1  
        