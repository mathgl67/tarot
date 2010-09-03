'''
Created on 8 juin 2010

@author: mathgl
'''

import os

from PyQt4 import QtGui, QtCore
from tarot.ui.generated.game import Ui_GameWindow
from tarot.ui.window.game_new import NewGameDialog
from tarot.ui.image.store import ImageStore
from tarot.ui.scene.hand import LittleHandScene
from tarot.contract import Contract

class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.ui.dockWidgetDog.setVisible(False)
        self.image_store = ImageStore(os.path.join("images", "cards"))
        
        self.game = None
        # slots
        #self.ui.pushButton.clicked.connect(self.actionNewActivated)
        self.connect(self.ui.actionNew, QtCore.SIGNAL("activated()"), self.newActivated)
        # hand click
        self.connect(self.ui.graphicsViewHandAll, QtCore.SIGNAL("clicked()"), self.clicked)
        # take click
        self.take_mapper = None
        self._init_take_mapper()
        # quit
        self.connect(self.ui.actionQuit, QtCore.SIGNAL("activated()"), self.close)
    
    def _init_take_mapper(self):
        """Connect button to mapper and mapper to take_clicked"""
        self.take_mapper = QtCore.QSignalMapper() 
        self.ui.pushButtonPass.clicked.connect(self.take_mapper.map)
        self.ui.pushButtonLittle.clicked.connect(self.take_mapper.map)
        self.ui.pushButtonGuard.clicked.connect(self.take_mapper.map)
        self.ui.pushButtonGuardAgainst.clicked.connect(self.take_mapper.map)
        self.ui.pushButtonGuardWithout.clicked.connect(self.take_mapper.map)
        self.take_mapper.setMapping(self.ui.pushButtonPass, 0)
        self.take_mapper.setMapping(self.ui.pushButtonLittle, 1)
        self.take_mapper.setMapping(self.ui.pushButtonGuard, 2)
        self.take_mapper.setMapping(self.ui.pushButtonGuardAgainst, 3)
        self.take_mapper.setMapping(self.ui.pushButtonGuardWithout, 4)
        
    def take_clicked(self, contract_type):
        print "ct:", contract_type    
    
    def clicked(self):
        print "clicked"    
    
    def newActivated(self):
        self.new_dialog = NewGameDialog()
        self.new_dialog.accepted.connect(self.newAccepted)
        self.new_dialog.exec_()
    
    def newAccepted(self):
        print "dialog accepted, create a new game..."
        self.game = self.new_dialog.get_result()
        self.distribute()
    
    def distribute(self):
        self.game.distribute()
        self.ui.dockWidgetHand.setEnabled(True)
        self.refresh_gui_hand()
        self.contract()
    
    def contract(self):
        print "contract"
        self.ui.dockWidgetTake.setEnabled(True)        
        self.game.contract = Contract(self.game.player_list)
        self.take_mapper.mapped.connect(self.game.contract.takeDecided)
        self.game.contract.finished.connect(self.contractFinished)
        self.game.contract.run()
        
    def contractFinished(self):
        print "contract finished"
        owner = self.game.contract.whoOwn()
        if not owner:
            #nobody take it
            self.distribute()
        else:
            if owner == self.game.getGuiPlayer():
                self.ui.dockWidgetDog.setVisible(True)
                self.refresh_gui_dog()
    
    def refresh_gui_dog(self):
        if self.game.dog:
            scene = LittleHandScene(self.game.dog, self.image_store)
            self.ui.graphicsViewDog.setScene(scene)
        else:
            self.ui.graphicsViewDog.setScene(None)
    
    def refresh_gui_hand(self):
        # split hand
        hand = self.game.getGuiPlayer().hand
        card_list = hand.split()
        #generate scene
        scene = {}
        scene["all"] = LittleHandScene(hand, self.image_store)
        for key, deck in card_list.iteritems():
            scene[key] = LittleHandScene(deck, self.image_store)
        
        self.ui.graphicsViewHandAll.setScene(scene["all"])
        self.ui.graphicsViewHandTrumps.setScene(scene["trumps_and_excuse"])
        self.ui.graphicsViewHandFaces.setScene(scene["faces"])
        self.ui.graphicsViewHandHearts.setScene(scene["hearts"])
        self.ui.graphicsViewHandDiamonds.setScene(scene["diamonds"])
        self.ui.graphicsViewHandSpades.setScene(scene["spades"])
        self.ui.graphicsViewHandClubs.setScene(scene["clubs"])
        