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

import os.path

from PyQt4 import QtGui
from tarot.game.card import Card, ExcuseCard, TrumpCard, FaceCard

class ImageStore(object):
    def __init__(self, base_path):
        self.base_path = base_path
        self.cache = {}
    
    def _get_path_for(self, card):
        path = None
        if isinstance(card, Card):
            path = os.path.join(card.suit, "%d.png" % card.number)
        elif isinstance(card, ExcuseCard):
            path = "excuse.png"
        elif isinstance(card, TrumpCard):
            path = os.path.join("trumps", "%d.png" % card.number)
        elif isinstance(card, FaceCard):
            path = os.path.join(card.suit, "%s.png" % card.name)
        return os.path.join(self.base_path, path)

    def pixmap_from_card(self, card):
        card_id = card.id()
        if not self.cache.has_key(card_id):
            self.cache[card_id] = QtGui.QPixmap(self._get_path_for(card))
        return self.cache[card_id]
    
