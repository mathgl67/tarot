'''
Created on 8 juin 2010

@author: mathgl
'''

from tarot.game.deck import DeckGeneration
from tarot.game.distribute import Distribute
from tarot.game.player import GuiPlayer, PlayerList

from PyQt4 import QtCore

class Game(QtCore.QObject):
    def __init__(self):
        super(Game, self).__init__()
        self.player_list = PlayerList()
        self.contract = None
        self.deck = DeckGeneration.full()
        self.deck.shuffle()
        self.dog = None
    
    def getGuiPlayer(self):
        for player in self.player_list.player_list:
            if isinstance(player, GuiPlayer):
                return player
    
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
    