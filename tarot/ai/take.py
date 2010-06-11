'''
Created on 6 juin 2010

@author: mathgl
'''

import math
from tarot.ai.test.runner import Runner
from tarot.ai.take_config_file import TakeConfigFile

class Take(object):
    def __init__(self, profile_name, player_count):
        self.take_config_file = TakeConfigFile("%s.ini" % profile_name)
        self.config = self.take_config_file.get_config(player_count)
        self.stats = self.take_config_file.get_stats(player_count)
        self.test_list = self.take_config_file.get_tests()
    
    def take(self, deck):
        runner = Runner(deck, self.test_list, self.config)
        runner.test()
        score = runner.ratio()
        (total_count, take_count) = self.stats
        moyen = float(take_count) / total_count
        test_count = len(self.test_list)
        
        moyen2 = math.pow(moyen, test_count)
        
        if score >= moyen2:
            return True
        return False
        