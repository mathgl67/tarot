'''
Created on 5 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui

from tarot.ui.image.deck import deck_to_card_item_list

class LittleHandScene(QtGui.QGraphicsScene):
    def __init__(self, deck, image_store, parent=None):
        super(LittleHandScene, self).__init__(parent)
        self.deck = deck
        self.image_store = image_store
        
        x=y=0
        pix_size = { "width": 221 * 0.35, "height": 391 * 0.35 }
        for card in deck_to_card_item_list(image_store, deck):
            card.setPos(x * pix_size["width"], y * pix_size["height"])
            card.scale(0.35, 0.35)
            self.addItem(card)
            # increment
            x += 1
                
    def get_margin_top(self):
        return 0

class HandScene(QtGui.QGraphicsScene):
    def __init__(self, title, deck, image_store, parent=None):
        super(HandScene, self).__init__(parent)
        self.deck = deck
        self.image_store = image_store
        
        x=y=0
        pix_size = { "width": 221 * 0.35, "height": 391 * 0.35 }
        
        deck_info = deck.informations()
        # add title on scene
        self.addText(title, QtGui.QFont("Helvsetica", 24)) 
        # add informations
        info1 = "Score: %.1f points - Bouts: %d/3" % (
            deck.score(),
            deck_info.count_bouts()
        )
        itm_info1 = self.addText(info1, QtGui.QFont("Helvsetica", 12))
        itm_info1.setPos(0, 37)

        info2 = "%d trumps (%.2f%% of hand, %.2f%% of game)" % (
            deck_info.count_trumps(),
            deck_info.deck_percentage_trumps(),
            deck_info.game_percentage_trumps()
        )
        itm_info2 = self.addText(info2, QtGui.QFont("Helvsetica", 12))
        itm_info2.setPos(0, 51)

        info3 = "%d faces (%.2f%% of hand, %.2f%% of game)" % (
            deck_info.count_faces(),
            deck_info.deck_percentage_faces(),
            deck_info.game_percentage_trumps()
        )
        itm_info3 = self.addText(info3, QtGui.QFont("Helvsetica", 12))
        itm_info3.setPos(0, 65)
        
        for card in deck_to_card_item_list(self.image_store, deck):
            card.setPos(x * pix_size["width"], 90 + y * pix_size["height"])
            card.scale(0.35, 0.35)
            self.addItem(card)
            # increment
            x += 1
            if x is 8:
                x = 0
                y += 1