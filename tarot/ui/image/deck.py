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

from PyQt4 import QtGui

class CardItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, image_store, card):
        super(CardItem, self).__init__()
        self.card = card
        self.setPixmap(image_store.pixmap_from_card(card))

    def mouseDoubleClickEvent(self, event):
        print "DoubleClic:", self.card

def deck_to_card_item_list(image_store, deck):
    list = []
    for card in deck.card_list:
            list.append(CardItem(image_store, card))
    return list
          
