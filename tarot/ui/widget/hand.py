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

from tarot.ui.scene.hand import LittleHandScene 

class HandWidget(QtCore.QObject):
    def __init__(self, window):
        QtCore.QObject.__init__(self)
        self.window = window
        self.image_store = self.window.image_store
        self.deck = None
        
        self.window.stream.input.game_deck.connect(self.set_hand)
        
    def set_hand(self, deck):
        self.deck = deck
        self.update()
    
    def update(self):
        self.scene = LittleHandScene(self.deck, self.image_store, self.window.ui.graphicsViewHand)
        self.window.ui.graphicsViewHand.setScene(self.scene)
        