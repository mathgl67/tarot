'''
Created on 8 juin 2010

@author: mathgl
'''

from tarot.player import AbstractPlayer

class DummyAiPlayer(AbstractPlayer):
    def take(self, turn_take):
        print "shoudl take?"
        self.takeDecided.emit(self.takeList["pass"])
    
    def turn(self, turn_deck):
        return None
    