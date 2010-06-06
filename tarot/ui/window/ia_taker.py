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

from tarot.ai.take_config_file import TakeConfigFile
from tarot.ai.test.runner import Runner

from tarot.distribute import Distribute
import tarot.card

class IATakerDb(object):
    def __init__(self, profile_name):
        self.db = sqlite3.connect("taker.db")
        self.profile_name = profile_name
        # load tests
        self.deck_test_config_file = TakeConfigFile("%s.ini" % profile_name)
        self.tests = self.deck_test_config_file.get_tests()
        # init table
        self.create_tables_if_not_exits()
        self.create_profile()
           
    def create_tables_if_not_exits(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(250) UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id NOT NULL,
                player_count INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER(11) NOT NULL,
                name VARCHAR(255) NOT NULL,
                result INTEGER(11) NOT NULL,
                take INTEGER(11) NOT NULL
            )
        """)
        
        self.db.commit()
        cursor.close()
    
    def create_profile(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM profile WHERE name=:name",
                       {"name": self.profile_name})
        
        row = cursor.fetchone()
        if row:
            self.profile_id = row[0] 
        else:
            print "create profile entry"
            cursor.execute("INSERT INTO profile (name) VALUES (:name)", 
                           {"name": self.profile_name})
            self.db.commit()
            self.profile_id = cursor.lastrowid
            
        cursor.close()
 
    def create_game(self, player_count):
        cursor = self.db.cursor()
        print "create game entry"
        cursor.execute("""
            INSERT INTO game (
                profile_id, player_count
            ) VALUES (
                :profile_id, :player_count
            )""", {
            "profile_id": self.profile_id,
            "player_count": player_count
        })
        self.db.commit()
            
        game_id = cursor.lastrowid
        cursor.close()
        return game_id
    
    def create_test_result(self, game_id, name, result, take):
        cursor = self.db.cursor()
        cursor.execute("""
                INSERT INTO test_result (
                    game_id, name, result, take)
                VALUES (
                    :game_id, :name, :result, :take
                )    
        """, {
              "game_id": game_id,
              "name": name,
              "result": 1 if result else 0,
              "take": take
        })
        self.db.commit()
        cursor.close()
    
    def take(self, player_count, deck, value):
        """value: 0(Pass), 1(Little), 2(Guard), 3(GuardAgainst), 4(GuardWithout)"""
        print "Take '%s' with %d" % (deck, value)
        runner = Runner(deck, self.tests)
        results = runner.test()
        
        game_id = self.create_game(player_count)
        for name, result in results.iteritems():
            self.create_test_result(game_id, name, result, value)

    def get_games(self, player_count):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM game WHERE profile_id=:profile_id AND player_count=:player_count",
                       {"profile_id": self.profile_id, "player_count": player_count})
        games = []
        for row in cursor:
            games.append(row[0])

        cursor.close()
        
        return games
    
    def save_config(self, player_count):
        print "save configuration.."
        self.deck_test_config_file.write_config(player_count, self.get_config(player_count))
    
    def get_config(self, player_count):
        cursor = self.db.cursor()
        
        games = self.get_games(player_count)
        
        results = {}
        for game_id in games:
            cursor.execute("SELECT name, result, take FROM test_result WHERE game_id = :game_id",
                           {"game_id": game_id})
            for row in cursor:
                if not results.has_key(row[0]):
                    results[row[0]] = 0
                if row[1] > 0:
                    results[row[0]] += 1
                    
        cursor.close()
        
        config = {}
        for key, value in results.iteritems():
            
            if value == 0 or value == len(games):
                adjustement = float(1) / len(games)
                if value == 0:
                    print "adjust + 1/games_count for '%s'" % (key)
                    value = adjustement
                else:
                    print "adjust - 1/games_count for '%s'" % (key)
                    value = 1 - adjustement
            
                
            config[key] = float(value) / len(games)
             
        return config
    
class IATakerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IATakerWindow, self).__init__()
        self.ui = Ui_IATaker()
        self.ui.setupUi(self)
        self.image_store = ImageStore(os.path.join("images", "cards"))
        self.take_db = IATakerDb("test")
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
        
    def pass_clicked(self):
        print "pass!"
        self.take_db.take(self.player_count, self.player_hand, 0)
        self.distribute(self.player_count)
        self.take_db.save_config(self.player_count)
        
    def little_clicked(self):
        print "little!"
        self.take_db.take(self.player_count, self.player_hand, 1)
        self.distribute(self.player_count)
        self.take_db.save_config(self.player_count)
        
    def garde_clicked(self):
        print "garde!"
        self.take_db.take(self.player_count, self.player_hand, 2)
        self.distribute(self.player_count)
        self.take_db.save_config(self.player_count)
        
    def garde_without_clicked(self):
        print "garde sans!"
        self.take_db.take(self.player_count, self.player_hand, 3)
        self.distribute(self.player_count)
        self.take_db.save_config(self.player_count)
        
    def garde_against_clicked(self):
        print "garde contre!"
        self.take_db.take(self.player_count, self.player_hand, 4)
        self.distribute(self.player_count)
        self.take_db.save_config(self.player_count)