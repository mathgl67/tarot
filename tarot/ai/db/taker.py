'''
Created on 7 juin 2010

@author: mathgl
'''

from tarot.ai.take_config_file import TakeConfigFile
from tarot.ai.test.runner import Runner
import sqlite3

class AiTakerDb(object):
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
                player_count INTEGER NOT NULL,
                take INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER(11) NOT NULL,
                name VARCHAR(255) NOT NULL,
                result INTEGER(11) NOT NULL
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
 
    def create_game(self, player_count, take):
        cursor = self.db.cursor()
        print "create game entry"
        cursor.execute("""
            INSERT INTO game (
                profile_id, player_count, take
            ) VALUES (
                :profile_id, :player_count, :take
            )""", {
            "profile_id": self.profile_id,
            "player_count": player_count,
            "take": take
        })
        self.db.commit()
            
        game_id = cursor.lastrowid
        cursor.close()
        return game_id
    
    def create_test_result(self, game_id, name, result):
        cursor = self.db.cursor()
        cursor.execute("""
                INSERT INTO test_result (
                    game_id, name, result
                ) VALUES (
                    :game_id, :name, :result
                )    
        """, {
              "game_id": game_id,
              "name": name,
              "result": 1 if result else 0,
        })
        self.db.commit()
        cursor.close()
    
    def take(self, player_count, deck, value):
        """value: 0(Pass), 1(Little), 2(Guard), 3(GuardAgainst), 4(GuardWithout)"""
        print "Take '%s' with %d" % (deck, value)
        runner = Runner(deck, self.tests)
        results = runner.test()
        
        game_id = self.create_game(player_count, value)
        for name, result in results.iteritems():
            self.create_test_result(game_id, name, result)

    def get_games_win(self, player_count):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM game WHERE profile_id=:profile_id AND player_count=:player_count AND take > 0",
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
        
        games = self.get_games_win(player_count)
        
        results = {}
        for game_id in games:
            cursor.execute("SELECT name, result FROM test_result WHERE game_id = :game_id",
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
