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

class Runner(object):
    def __init__(self, deck, tests=None, config=None):
        self.deck = deck
        self.tests = tests if tests else {}
        self.config = config if config else {}
        self.results = {}
            
    def test(self):
        for name, test in self.tests.iteritems():
            self.results[name] = test.test(self.deck)
        return self.results

    def ratio(self):
        ratio = 1
        for name, result in self.results.iteritems():
            if not (self.config.has_key("%s-true" % name) and
                    self.config.has_key("%s-false" % name)):
                print "WARNING: test '%s' as no config!" % name
                continue
                    
            if result:
                r = self.config["%s-true" % name]
            else:
                r = self.config["%s-false" % name]
            ratio *= r
            
        return ratio
