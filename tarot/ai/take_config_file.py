'''
Created on 6 juin 2010

@author: mathgl
'''
from ConfigParser import RawConfigParser
from tarot.ai.test.deck import BoutCountDeckTest, TrumpPercentageOfDeckTest
from tarot.ai.test.deck import CutCountDeckTest, FaceCountByNameDeckTest
from tarot.ai.test.deck import FaceScoreDeckTest, ScoreDeckTest
from tarot.ai.test.deck import TrumpCountDeckTest

class TakeConfigFile(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.classes_name = {
            "bout_count": BoutCountDeckTest,
            "trump_percentage_of_deck": TrumpPercentageOfDeckTest,
            "cut_count": CutCountDeckTest,
            "face_count_by_name": FaceCountByNameDeckTest,
            "face_score": FaceScoreDeckTest,
            "score": ScoreDeckTest,
            "trump_count": TrumpCountDeckTest,
        }
    
    @staticmethod
    def parse_function_and_args(string):
        array = string.split(":")
        
        if len(array) < 1:
            print "WARNING: test is unspecified (%s)" % string
            return (None, None)
        
        if len(array) < 2:
            print "WARNING: test has no arguments (%s)" % string
            return (array[0], None)
        
        return (array[0], array[1])
    
    def load_config(self):
        config = RawConfigParser()
        config.read(self.config_file)
        return config
    
    def get_tests(self):
        config = self.load_config()
        test_dict = {}
        for key, value in config.items("taker-tests"):
            (name, param) = self.parse_function_and_args(value)
            if not self.classes_name.has_key(name):
                print "WARNING: function '%s' unknown." % name
                continue
            test = self.classes_name[name]()
            test.parse_config(param)
            test_dict[key] = test
        
        return test_dict
    
    def write_config(self, player_count, ratio_dict):
        config = self.load_config()
        section = "taker-config-%dp" % player_count
        #add section if not exists
        if not config.has_section(section):
            config.add_section(section)
        #set configuration
        for key, value in ratio_dict.iteritems():
            config.set(section, key, value)
        #write file
        config.write(file(self.config_file, "w+"))

    def get_config(self, player_count):
        config = self.load_config()
        section = "taker-config-%dp" % player_count
        if not config.has_section(section):
            print "WARNING: configuration has no section '%s" % (section)
            return {}
        
        ratio_dict = {}
        for key, value in config.items(section):
            ratio_dict[key] = float(value)
            
        return ratio_dict 