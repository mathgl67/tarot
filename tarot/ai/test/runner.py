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
            if not self.config.has_key(name):
                print "WARNING: test '%s' as no config!" % name
                continue
            
            if self.config[name] == 0.0: # ratio == 0 dangerous ?
                print "WARNING: test '%s' configuration ratio is 0!" % name
                continue
            #if self.config[name] <= 0.5:
            #    print "WARNING: test '%s' configuration ratio <= 0.5" % name
            #    continue
            if self.config[name] == 1.0: # ratio == 1 dangerous ?
                print "WARNING: test '%s' configuration ratio is 1!" % name
                continue
            
            if result:
                r = self.config[name]
            else:
                r = 1 - self.config[name]
            ratio *= r
            
        return ratio
