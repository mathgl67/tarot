'''
Created on 5 juin 2010

@author: mathgl
'''

import os
import sqlite3

from PyQt4 import QtGui, QtCore
from tarot.ui.scene.hand import HandScene
from tarot.ui.generated.ia_taker import Ui_IATaker
from tarot.ui.image.store import ImageStore

from tarot.ai.test.runner import a_test_list, Runner

from tarot.distribute import Distribute
import tarot.card

class IATakerDb(object):
    def __init__(self):
        self.db = sqlite3.connect("taker.db")
        self.profile_name = "default"
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                name VARCHAR(250) NOT NULL,
                PRIMARY KEY(name)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS score (
                id BIGINT AUTO_INCREMENT,
                profile_name VARCHAR(250) NOT NULL,
                test VARCHAR(250),
                result INTEGER,
                value INTEGER,
                PRIMARY KEY(id)
            )
        """)
        self.cursor.execute("""SELECT count(*) FROM profile WHERE name=?""", (self.profile_name,))
        profile_exists = False
        for row in self.cursor:
            if row[0] == 1:
                profile_exists = True
        
        if not profile_exists:
            print "create entry"
            self.cursor.execute("""INSERT INTO profile (name) VALUES (?)""", (self.profile_name,))
        
        self.db.commit()
    
    def take(self, deck, value):
        """value: 0(Pass), 1(Little), 2(Guard), 3(GuardAgainst), 4(GuardWithout)"""
        print "Take '%s' with %d" % (deck, value)
        r = Runner(deck, a_test_list())
        res = r.test()
        for t, v in res.iteritems():
            self.cursor.execute("""
                INSERT INTO score (profile_name, test, result, value) VALUES (?,?,?,?) 
            """, (self.profile_name, t, 1 if v else 0, value))
        self.db.commit()

class IATakerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IATakerWindow, self).__init__()
        self.ui = Ui_IATaker()
        self.ui.setupUi(self)
        self.image_store = ImageStore(os.path.join("images", "cards"))
        self.take_db = IATakerDb()
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
        card_list = tarot.card.generate_tarot_cards()
        tarot.card.shuffle_cards(card_list)

        distribute = Distribute(card_list, player_count)
 
        player_list = distribute.do()[0]

        #create scenes
        self.player_hand = player_list[0]
        self.player_scene = HandScene("Hand", self.player_hand, self.image_store, self.ui.GraphicView)

        #set scene to player 1
        self.ui.GraphicView.setScene(self.player_scene)
        self.number_of_player = player_count 

    def distribute_3p_activated(self):
        print "Distribute for 3 players..."
        self.distribute(3)

    def distribute_4p_activated(self):
        print "Distribute for 4 players..."
        self.distribute(4)

    def distribute_5p_activated(self):
        print "Distribute for 5 players..."
        self.distribute(5)
        
    def pass_clicked(self):
        print "pass!"
        self.take_db.take(self.player_hand, 0)
        self.distribute(self.number_of_player)
        
    def little_clicked(self):
        print "little!"
        self.take_db.take(self.player_hand, 1)
        self.distribute(self.number_of_player)
        
    def garde_clicked(self):
        print "garde!"
        self.take_db.take(self.player_hand, 2)
        self.distribute(self.number_of_player)
        
    def garde_without_clicked(self):
        print "garde sans!"
        self.take_db.take(self.player_hand, 3)
        self.distribute(self.number_of_player)
        
    def garde_against_clicked(self):
        print "garde contre!"
        self.take_db.take(self.player_hand, 4)
        self.distribute(self.number_of_player)
        