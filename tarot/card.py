#! /usr/bin/env python

import random
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

    def score(self):
	return 0.5

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

    def score(self):
	if self.name == "king":
		return 4.5
	elif self.name == "queen":
		return 3.5
	elif self.name == "knight":
		return 2.5
	# you are jack
	return 1.5

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

    def score(self):
	if self.is_bout():
		return 4.5
	return 0.5

    def is_bout(self):
	if self.number is 1 or self.number is 21:
		return True
	return False

class ExcuseCard(AbstractCard):
    def _get_pixmap(self):
	return QtGui.QPixmap("images/cards/excuse.png")

    def __repr__(self):
        return "ExcuseCard()"

    def score(self):
	return 4.5

    def is_bout(self):
	return True	

def generate_suit(suit_name):
    suit = []
    for number in range(1,11):
        suit.append(Card(suit_name, number))

    for face_card in ["jack", "knight", "queen", "king"]:
        suit.append(FaceCard(suit_name, face_card))

    return suit

def generate_trumps():
    trumps = []
    for number in range(1,22):
        trumps.append(TrumpCard(number))

    return trumps

def generate_tarot_cards():
    tarot_cards = []
    for suit_name in ["diamons", "clubs", "hearts", "spades"]:
	tarot_cards.extend(generate_suit(suit_name))

    tarot_cards.extend(generate_trumps())
    tarot_cards.append(ExcuseCard())
    return tarot_cards 

def shuffle_cards(cards):
    random.shuffle(cards)

