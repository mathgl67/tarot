#! /usr/bin/env python

from PyQt4 import QtGui

class AbstractCard(QtGui.QGraphicsPixmapItem):
    def __init__(self):
	super(AbstractCard, self).__init__()
	self.setPixmap(self._get_pixmap())

    def _get_pixmap(self):
	return QtGui.QPixmap("images/cards/empty.png")

    def is_bout(self):
	return False

class Card(AbstractCard):
    def __init__(self, suit, number):
	self.suit = suit
	self.number = number
	super(Card, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap(
		"images/cards/%s/%d.png" % (self.suit, self.number)
	)

    def __repr__(self):
        return "Card(suit=%s,number=%d)" % (
            self.suit,
            self.number
        )

class FaceCard(AbstractCard):
    def __init__(self, suit, name):
	self.suit = suit
        self.name = name
        super(FaceCard, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap(
		"images/cards/%s/%s.png" % (self.suit, self.name)
	)

    def __repr__(self):
        return "FaceCard(suit=%s,name=%s)" % (
	    self.suit,
            self.name
        )

class TrumpCard(AbstractCard):
    def __init__(self, number):
	self.number = number
	super(TrumpCard, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap("images/cards/trumps/%d.png" % self.number)

    def __repr__(self):
        return "TrumpCard(number=%d)" % (self.number)

    def is_bout(self):
	if self.number is 1 or self.number is 21:
		return True
	return False

class ExcuseCard(AbstractCard):
    def _get_pixmap(self):
	return QtGui.QPixmap("images/cards/excuse.png")

    def __repr__(self):
        return "ExcuseCard()"

    def is_bout(self):
	return True	

