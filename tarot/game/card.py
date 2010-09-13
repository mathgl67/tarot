# -*- coding: utf-8 -*-

class AbstractCard(object):
    def id(self):
        return None
    
    def is_bout(self):
        return False

class Card(AbstractCard):
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        super(Card, self).__init__()

    def id(self):
        return "%s-%d" % (self.suit, self.number)

    def score(self):
        return 0.5

    def __repr__(self):
        return "Card(suit=%s,number=%d)" % (self.suit, self.number)

class FaceCard(AbstractCard):
    def __init__(self, suit, name):
        self.suit = suit
        self.name = name
        super(FaceCard, self).__init__()

    def id(self):
        return "%s-%s" % (self.suit, self.name)

    def score(self):
        if self.name == "king":
            return 4.5
        elif self.name == "queen":
            return 3.5
        elif self.name == "knight":
            return 2.5
        elif self.name == "jack":
            return 1.5

    def __repr__(self):
        return "FaceCard(suit=%s,name=%s)" % (
        self.suit,
            self.name
        )

class TrumpCard(AbstractCard):
    def __init__(self, number):
        self.number = number
        super(TrumpCard, self).__init__()

    def __repr__(self):
        return "TrumpCard(number=%d)" % (self.number)

    def id(self):
        return "trump-%d" % (self.number)

    def score(self):
        if self.is_bout():
            return 4.5
        return 0.5

    def is_bout(self):
        if self.number is 1 or self.number is 21:
            return True
        return False

class ExcuseCard(AbstractCard):
    def __repr__(self):
        return "ExcuseCard()"

    def id(self):
        return "excuse"

    def score(self):
        return 4.5

    def is_bout(self):
        return True
