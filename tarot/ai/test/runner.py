'''
Created on 4 juin 2010

@author: mathgl
'''

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
