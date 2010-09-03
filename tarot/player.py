'''
Created on 8 juin 2010

@author: mathgl
'''

from PyQt4 import QtCore

class PlayerList(QtCore.QObject):
    def __init__(self):
        self.player_list = []
        self.player_count = 0
        self.distributer = None
        
    def append(self, player):
        # define id and order to sort the list
        player.id = self.player_count
        player.order = self.player_count
        # increment player_count to have a length cache
        self.player_count +=1
        # finally append to list
        self.player_list.append(player)
    
    def __repr__(self):
        player_str = []
        for player in self.player_list:
            player_str.append(repr(player))
        return "PlayerList(%s)" % (",".join(player_str))
    
    def next(self):
        for player in self.player_list:
            yield player
    
    def reorder(self, player_first):
        adjustement = self.player_count - player_first.order
        for player in self.player_list:           
            player.order = (player.order + adjustement) % self.player_count
        self.player_list = sorted(self.player_list, key=lambda p: p.order)        

    def getPlayerAfter(self, player):
        next_order = (player.order + 1) % self.player_count
        for p in self.next():
                if p.order == next_order:
                    return p
        return None
    
    def nextDistributer(self):
        if not self.distributer:
            # this should not append and first distributer should be
            # handle by another way
            self.distributer = self.player_list[0]
        else:
            self.distributer = self.getPlayerAfter(self.distributer)
    
class AbstractPlayer(QtCore.QObject):
    
    takeList = { "pass": 0, "little": 1, "guard": 2, "guard against": 3, "guard without": 4 }
    
    takeDecided = QtCore.pyqtSignal(int)
    turnDecided = QtCore.pyqtSignal()
    
    def __init__(self, name=None):
        super(AbstractPlayer,self).__init__()
        self.id = 0
        self.name = name
        self.type = None
        self.order = 0
        self.score = 0
        self.hand = None
    
    def __repr__(self):
        return "Player(%s)" % self.name
    
    def take(self, turn_take):
        pass
        
    def turn(self, turn_deck):
        pass

class GuiPlayer(AbstractPlayer):
    def __init__(self, name=None):
        super(GuiPlayer, self).__init__(name)
        self.type = "GuiPlayer"
    
    def take(self, contract):
        print contract
        print "player should say if he take"
        
    def turn(self, turn_deck):
        self.turn_deck = turn_deck
        print "player should say what he play"
        return None
    
