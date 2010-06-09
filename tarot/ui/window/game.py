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

class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.image_store = ImageStore(os.path.join("images", "cards"))
        
        self.game = None
        # slots
        #self.ui.pushButton.clicked.connect(self.actionNewActivated)
        self.connect(self.ui.actionNew, QtCore.SIGNAL("activated()"), self.newActivated)
        # hand display/hide
        self.ui.dockWidgetHand.visibilityChanged.connect(self.handVisibilityChanged)
        self.ui.actionHand.changed.connect(self.handShowHide)
        self.ui.dockWidgetTake.visibilityChanged.connect(self.takeVisibilityChanged)
        self.ui.actionTake.changed.connect(self.takeShowHide)
        # hand click
        self.connect(self.ui.graphicsViewHandAll, QtCore.SIGNAL("clicked()"), self.clicked)
        # quit
        self.connect(self.ui.actionQuit, QtCore.SIGNAL("activated()"), self.close)
        
    def clicked(self):
        print "clicked"    
    
    def newActivated(self):
        self.new_dialog = NewGameDialog()
        self.new_dialog.accepted.connect(self.newAccepted)
        self.new_dialog.exec_()
    
    def newAccepted(self):
        print "dialog accepted, create a new game..."
        self.game = self.new_dialog.get_result()
        self.game.distribute()
        self.refresh_gui_hand()
        
    def handVisibilityChanged(self, value):
        self.ui.actionHand.setChecked(value)
        
    def handShowHide(self):
        if self.ui.actionHand.isChecked():
            self.ui.dockWidgetHand.show()
        else:
            self.ui.dockWidgetHand.hide()
            
    def takeVisibilityChanged(self, value):
        self.ui.actionTake.setChecked(value)
    
    def takeShowHide(self):
        if self.ui.actionTake.isChecked():
            self.ui.dockWidgetTake.show()
        else:
            self.ui.dockWidgetTake.hide()
        
    def refresh_gui_hand(self):
        # split hand
        hand = self.game.getGuiPlayer().hand
        card_list = hand.split()
        #generate scene
        scene = {}
        scene["all"] = LittleHandScene(hand,self.image_store)
        for key, deck in card_list.iteritems():
            scene[key] = LittleHandScene(deck, self.image_store)
        
        self.ui.graphicsViewHandAll.setScene(scene["all"])
        self.ui.graphicsViewHandTrumps.setScene(scene["trumps_and_excuse"])
        self.ui.graphicsViewHandFaces.setScene(scene["faces"])
        self.ui.graphicsViewHandHearts.setScene(scene["hearts"])
        self.ui.graphicsViewHandDiamonds.setScene(scene["diamonds"])
        self.ui.graphicsViewHandSpades.setScene(scene["spades"])
        self.ui.graphicsViewHandClubs.setScene(scene["clubs"])
        