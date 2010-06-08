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
        
    def newActivated(self):
        self.new_dialog = NewGameDialog()
        self.new_dialog.accepted.connect(self.newAccepted)
        self.new_dialog.exec_()
    
    def newAccepted(self):
        print "dialog accepted, create a new game..."
        self.game = self.new_dialog.get_result()
        self.game.distribute()
        self.refresh_gui_hand()
        
    def refresh_gui_hand(self):
        scene = LittleHandScene(self.game.getGuiPlayer().hand, self.image_store) 
        self.ui.graphicsViewHandAll.setScene(scene)
        