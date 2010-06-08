'''
Created on 8 juin 2010

@author: mathgl
'''

from tarot.deck import DeckGeneration
from tarot.distribute import Distribute
from tarot.player import GuiPlayer

class Game(object):
    def __init__(self, player_count):
        self.player_count = player_count
        self.player_list = []
        self.player_distrib = 0
    
        self.deck = DeckGeneration.full()
        self.dog = None
    
    def getGuiPlayer(self):
        for player in self.player_list:
            if isinstance(player, GuiPlayer):
                return player
    
    def distribute(self):
        distribute = Distribute(self.deck, self.player_count)
        (player_deck_list, self.dog) = distribute.do()
        
        for i in range(0, self.player_count):
            self.player_list[i].hand = player_deck_list[i]
            
    