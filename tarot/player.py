'''
Created on 8 juin 2010

@author: mathgl
'''

class AbstractPlayer(object):
    
    take = { "pass": 0, "little": 1, "guard": 2, "guard sans": 3, "guard contre": 4 }
    
    def __init__(self, name=None):
        self.name = name
        self.type = None
        self.score = 0
        self.hand = None
    
    def take(self, turn_take):
        pass
    
    def turn(self, turn_deck):
        pass

class GuiPlayer(AbstractPlayer):
    def __init__(self, name=None):
        super(GuiPlayer, self).__init__(name)
        self.type = "GuiPlayer"
    
    def take(self, turn_take):
        print "player should say if he take"
        return self.take["pass"]
    
    def turn(self, turn_deck):
        print "player should say what he play"
        return None
    
