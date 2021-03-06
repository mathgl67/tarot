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

class AbstractDeckTest(object):
    def __init__(self, config=None):
        self.config = config if config else {}
    
    @staticmethod
    def _do_test_name(test, a, b):
        if test == "<":
            return a < b
        elif test == "<=":
            return a <= b
        elif test == "==":
            return a == b
        elif test == ">=":
            return a >= b
        elif test == ">":
            return a > b

    def parse_config_value(self, name, value):
        """Default parse
            - value is integer
        """
        if name == "value":
            return int(value)
        
        return value

    def parse_config(self, string):
        """Basic param1(value1),param2(value2) parser"""
        comma_array = string.split(",")
        for param in comma_array:
            bracket_array =  param.split("(")
            if len(bracket_array) != 2:
                print "WARNING: param or value not found (%s)" % param
                continue
            name = bracket_array[0]
            value = bracket_array[1][0:-1] # Remove ending )
            
            self.config[name] = self.parse_config_value(name, value)
        
    def test(self, deck):
        return False

class BoutCountDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().count_bouts(),
                                  self.config["value"]
                                  )
class CutCountDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().count_cuts(),
                                  self.config["value"])
        
class TrumpCountDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().count_trumps(),
                                  self.config["value"]
                                  )

class TrumpPercentageOfDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().deck_percentage_trumps(),
                                  self.config["value"]
                                  )
        
class FaceCountByNameDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().count_face_is(self.config["name"]),
                                  self.config["value"]
                                  )

class FaceScoreDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().score_faces(),
                                  self.config["value"]
                                  )

class ScoreDeckTest(AbstractDeckTest):    
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.score(),
                                  self.config["value"]
                                  )

class BoutNameIsInDeckTest(AbstractDeckTest):
    def test(self, deck):
        return deck.informations().have_bout_name(self.config["name"])            


class TrumpCountSupDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
                                  self.config["test"],
                                  deck.informations().count_trump_sup(int(self.config["number"])),
                                  self.config["value"]
                                  )
    
class FaceSuiteCountDeckTest(AbstractDeckTest):
    def test(self, deck):
        return self._do_test_name(
            self.config["test"],
            deck.informations().count_face_suite(),
            self.config["value"]
        )                                              