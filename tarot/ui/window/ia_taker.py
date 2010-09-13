'''
Created on 5 juin 2010

@author: mathgl
'''

import os

from PyQt4 import QtGui, QtCore
from tarot.ui.scene.hand import HandScene
from tarot.ui.generated.ia_taker import Ui_IATaker
from tarot.ui.image.store import ImageStore
from tarot.ai.db.taker import AiTakerDb

from tarot.game.distribute import Distribute
from tarot.game.deck import DeckGeneration
    
class IATakerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IATakerWindow, self).__init__()
        self.ui = Ui_IATaker()
        self.ui.setupUi(self)
        self.image_store = ImageStore(os.path.join("images", "cards"))
        self.take_db = AiTakerDb("test")
        # signals
        QtCore.QObject.connect(
            self.ui.Distribute_3P,
            QtCore.SIGNAL("activated()"),
            self.distribute_3p_activated
        )

        QtCore.QObject.connect(
            self.ui.Distribute_4P,
            QtCore.SIGNAL("activated()"),
            self.distribute_4p_activated
        )

        QtCore.QObject.connect(
            self.ui.Distribute_5P,
            QtCore.SIGNAL("activated()"),
            self.distribute_5p_activated
        )
        
        QtCore.QObject.connect(
            self.ui.actionSave,
            QtCore.SIGNAL("activated()"),
            self.actionSaveActivated
        )
        
        QtCore.QObject.connect(
            self.ui.Pass,
            QtCore.SIGNAL("clicked()"),
            self.pass_clicked
        )
        
        QtCore.QObject.connect(
            self.ui.Little,
            QtCore.SIGNAL("clicked()"),
            self.little_clicked
        )
        
        QtCore.QObject.connect(
            self.ui.Garde,
            QtCore.SIGNAL("clicked()"),
            self.garde_clicked
        )
        
        QtCore.QObject.connect(
            self.ui.GardeAgainst,
            QtCore.SIGNAL("clicked()"),
            self.garde_against_clicked
        )
        
        QtCore.QObject.connect(
            self.ui.GardeWithout,
            QtCore.SIGNAL("clicked()"),
            self.garde_without_clicked
        )
        self.distribute(3)
        
    def distribute(self, player_count):
        deck = DeckGeneration.full()
        deck.shuffle()

        distribute = Distribute(deck, player_count)
 
        player_list = distribute.do()[0]

        #create scenes
        self.player_hand = player_list[0]
        self.player_scene = HandScene("Hand", self.player_hand, self.image_store, self.ui.GraphicView)

        #set scene to player 1
        self.ui.GraphicView.setScene(self.player_scene)
        self.player_count = player_count

    def distribute_3p_activated(self):
        print "Distribute for 3 players..."
        self.distribute(3)

    def distribute_4p_activated(self):
        print "Distribute for 4 players..."
        self.distribute(4)

    def distribute_5p_activated(self):
        print "Distribute for 5 players..."
        self.distribute(5)
    
    def actionSaveActivated(self):
        print "save"
        self.take_db.save_config(self.player_count)
    
    def pass_clicked(self):
        print "pass!"
        self.take_db.take(self.player_count, self.player_hand, 0)
        self.distribute(self.player_count)
        
    def little_clicked(self):
        print "little!"
        self.take_db.take(self.player_count, self.player_hand, 1)
        self.distribute(self.player_count)
        
    def garde_clicked(self):
        print "garde!"
        self.take_db.take(self.player_count, self.player_hand, 2)
        self.distribute(self.player_count)
        
    def garde_without_clicked(self):
        print "garde sans!"
        self.take_db.take(self.player_count, self.player_hand, 3)
        self.distribute(self.player_count)
        
    def garde_against_clicked(self):
        print "garde contre!"
        self.take_db.take(self.player_count, self.player_hand, 4)
