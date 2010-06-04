'''
Created on 4 juin 2010

@author: mathgl
'''

import os.path

from PyQt4 import QtGui
from tarot.card import Card, ExcuseCard, TrumpCard, FaceCard

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
    