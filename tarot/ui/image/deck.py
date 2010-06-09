'''
Created on 4 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui, QtCore
from tarot.card import AbstractCard

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
          
