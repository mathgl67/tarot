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
                                  deck.informations.count_trumps(),
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
