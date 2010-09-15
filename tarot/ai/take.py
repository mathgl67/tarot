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
        