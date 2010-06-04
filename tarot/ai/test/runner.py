'''
Created on 4 juin 2010

@author: mathgl
'''

from tarot.ai.test.deck import BoutCountDeckTest, CutCountDeckTest
from tarot.ai.test.deck import TrumpPercentageOfDeckTest, FaceCountByNameDeckTest

def a_test_list():
    tests = {}
    # bouts
    tests["bout_count_==_1"] = BoutCountDeckTest({"test": "==", "value": 1})
    tests["bout_count_==_2"] = BoutCountDeckTest({"test": "==", "value": 2})
    tests["bout_count_==_3"] = BoutCountDeckTest({"test": "==", "value": 3})
       
    # trumps
    tests["trump_percentage_of_deck_<_10"] = TrumpPercentageOfDeckTest({"test": "<", "value": 10})
    tests["trump_percentage_of_deck_<_20"] = TrumpPercentageOfDeckTest({"test": "<", "value": 20})
    tests["trump_percentage_of_deck_<_30"] = TrumpPercentageOfDeckTest({"test": "<", "value": 30})
    tests["trump_percentage_of_deck_<_40"] = TrumpPercentageOfDeckTest({"test": "<", "value": 40})
    tests["trump_percentage_of_deck_<_50"] = TrumpPercentageOfDeckTest({"test": "<", "value": 50})
    tests["trump_percentage_of_deck_>_50"] = TrumpPercentageOfDeckTest({"test": ">", "value": 50})
       
    # cuts
    tests["cut_count_==_1"] = CutCountDeckTest({"test": "==", "value": 1})
    tests["cut_count_==_2"] = CutCountDeckTest({"test": "==", "value": 2})
    tests["cut_count_==_3"] = CutCountDeckTest({"test": "==", "value": 3})
    tests["cut_count_==_4"] = CutCountDeckTest({"test": "==", "value": 4})
          
    # faces              
    tests["face_count_name_is_king_=<_2"] = FaceCountByNameDeckTest({"name": "king", "test": "<=", "value": 2})
    tests["face_count_name_is_king_>_2"] = FaceCountByNameDeckTest({"name": "king", "test": ">", "value": 2})
    tests["face_count_name_is_queen_=<_2"] = FaceCountByNameDeckTest({"name": "queen", "test": "<=", "value": 2})
    tests["face_count_name_is_queen_>_2"] = FaceCountByNameDeckTest({"name": "queen", "test": ">", "value": 2})
    tests["face_count_name_is_knight_=<_2"] = FaceCountByNameDeckTest({"name": "knight", "test": "<=", "value": 2})
    tests["face_count_name_is_knight_>_2"] = FaceCountByNameDeckTest({"name": "knight", "test": ">", "value": 2})
    tests["face_count_name_is_jack_=<_2"] = FaceCountByNameDeckTest({"name": "jack", "test": "<=", "value": 2})
    tests["face_count_name_is_jack_>_2"] = FaceCountByNameDeckTest({"name": "jack", "test": ">", "value": 2})               

    return tests


class Runner(object):
    def __init__(self, deck, tests={}, ratio=None):
        self.deck = deck
        self.tests = tests if tests else {}
        self.ratio = ratio if ratio else {}
        self.results = {}
            
    def test(self):
        for name, test in self.tests.iteritems():
            self.results[name] = test.test(self.deck)
        return self.results

    def ratio(self):
        ratio = 1
        for name, result in self.results.iteritems():
            if result:
                r = self.ratio[name]
            else:
                r = 1 - self.ratio[name]
            ratio *= r
        return ratio
