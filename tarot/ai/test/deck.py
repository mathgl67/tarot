'''
Created on 4 juin 2010

@author: mathgl
'''

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
