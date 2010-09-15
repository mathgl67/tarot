#
# -*- coding: utf8 -*-
#
# Tarot 
# Copyright (C) 2009-2010  mathgl67@gmail.com
#
#  This file is part of Tarot
#
#  Tarot is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Tarot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Tarot.  If not, see <http://www.gnu.org/licenses/>.
#

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
        #get stats
        (count_total, count_take) = self.db_state(player_count)
        
        self.deck_test_config_file.write_config(player_count, count_total, count_take, self.get_config(player_count))
    
    def get_config(self, player_count):
        cursor = self.db.cursor()
        
        config = {}
        for test_name in self.tests.iterkeys():
            # count_where_a_test_is_true
            cursor.execute("""
            SELECT 
                count(*)
            FROM 
                test_result
             WHERE 
                 name = :test_name AND 
                 result = 1
            """, {
                    "test_name": test_name
            })
            row = cursor.fetchone()
            count_test_true = row[0]
            # count_where_a_test_is_true_and_take
            cursor.execute("""
            SELECT
                count(*)
            FROM
                test_result 
            INNER JOIN
                game ON game_id = game.id
            WHERE
                name = :test_name AND
                result = 1 AND
                game.take > 0
            """, {
                  "test_name": test_name
            })
            row = cursor.fetchone()
            count_test_true_and_take = row[0]
               
            if not count_test_true == 0:       
                config["%s-true" % test_name] = float(count_test_true_and_take) / count_test_true
            
            # count_where_a_test_is_true
            cursor.execute("""
            SELECT 
                count(*)
            FROM 
                test_result
             WHERE 
                 name = :test_name AND 
                 result = 0
            """, {
                    "test_name": test_name
            })
            row = cursor.fetchone()
            count_test_false = row[0]
            # count_where_a_test_is_true_and_take
            cursor.execute("""
            SELECT
                count(*)
            FROM
                test_result 
            INNER JOIN
                game ON game_id = game.id
            WHERE
                name = :test_name AND
                result = 0 AND
                game.take > 0
            """, {
                  "test_name": test_name
            })
            row = cursor.fetchone()
            count_test_false_and_take = row[0]
            if not count_test_false == 0:       
                config["%s-false" % test_name] = float(count_test_false_and_take) / count_test_false      
            
        print "config", config
            
        return config
    
    def db_state(self, player_count):
        cursor = self.db.cursor()
        
        query_param = {"player_count": player_count}
        
        cursor.execute("SELECT count(*) FROM game WHERE player_count=:player_count", query_param)
        row = cursor.fetchone()
        count_total = row[0]
        
        cursor.execute("SELECT count(*) FROM game WHERE take > 0 AND player_count=:player_count", query_param)
        row = cursor.fetchone()
        count_take = row[0]
        
        return (count_total, count_take)
    
    def get_config2(self, player_count):
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
