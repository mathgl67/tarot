#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
 
from PyQt4 import QtGui
from tarot.deck import Deck
from tarot.card import Card, TrumpCard, FaceCard, ExcuseCard

app = QtGui.QApplication(sys.argv)

deck1 = Deck([
  Card("hearts", 5),
  Card("hearts", 6),
  Card("hearts", 9),
  ExcuseCard(),
  TrumpCard(1),
  FaceCard("hearts", "king"),
  FaceCard("hearts", "queen"),
  Card("clubs", 2),
  Card("clubs", 8),
  FaceCard("clubs", "queen"),#10
  Card("diamons", 6),
  Card("diamons", 7),
  TrumpCard(9),
  TrumpCard(10),
  TrumpCard(15),
])

deck2 = Deck([
  Card("hearts", 5),
  Card("hearts", 6),
  Card("hearts", 9),
  FaceCard("hearts", "king"),
  FaceCard("hearts", "queen"),
  Card("clubs", 1),
  Card("clubs", 2),
  Card("clubs", 8),
  FaceCard("clubs", "king"),
  Card("diamons", 3), #10
  Card("diamons", 4),
  Card("diamons", 6),
  Card("diamons", 7),
  Card("diamons", 8),
  Card("diamons", 10)
])

deck3 = Deck([
  Card("hearts", 5),
  Card("hearts", 6),
  Card("hearts", 9),
  FaceCard("hearts", "jack"),
  FaceCard("hearts", "queen"),
  Card("clubs", 1),
  Card("clubs", 2),
  Card("clubs", 8),
  FaceCard("clubs", "king"),
  Card("diamons", 3), #10
  Card("diamons", 4),
  Card("diamons", 6),
  Card("diamons", 7),
  Card("spades", 8),
  Card("spades", 10)
])

deck4 = Deck([
  TrumpCard(21),
  ExcuseCard(),
  Card("hearts", 6),
  Card("hearts", 9),
  FaceCard("hearts", "jack"),
  FaceCard("hearts", "queen"),
  FaceCard("hearts", "king"),
  TrumpCard(9),
  FaceCard("spades", "knight"),
  FaceCard("clubs", "king"),
  FaceCard("diamons", "queen"),
  Card("diamons", 7),
  Card("clubs", 8),
  Card("spades", 10)
])

deck5 = Deck([ # max
  ExcuseCard(),
  TrumpCard(21),
  TrumpCard(19),
  TrumpCard(18),
  TrumpCard(17),
  TrumpCard(16),
  TrumpCard(15),
  TrumpCard(14),
  TrumpCard(13),
  TrumpCard(12),
  FaceCard("spades", "king"),
  FaceCard("clubs", "king"),
  FaceCard("hearts", "king"),
  FaceCard("hearts", "queen"),
  FaceCard("clubs", "queen"),
])

deck6 = Deck([
  ExcuseCard(),
  TrumpCard(1),
  TrumpCard(2),
  TrumpCard(3),
  TrumpCard(4),
  TrumpCard(5),
  TrumpCard(6),
  Card("diamons", 10),
  Card("diamons", 9),
  Card("diamons", 8),
  Card("hearts", 10),
  Card("hearts", 10),
  Card("spades", 10),
  Card("spades", 9),
  Card("clubs", 10),
])

class AbstractRatioIteration(object):
    def __init__(self, config):
      self.config = config
    
    @staticmethod
    def _test(test, a, b):
      if test == "<":
	return a < b
      elif test == "<=":
	return a <= b
      elif test == "==":
	return a == b
      elif test == ">=":
	return a >= b
      elif test == ">":
	return a > b

    @staticmethod
    def test(test, ratio, a, b):
      if AbstractRatioIteration._test(test, a, b):
	return ratio
      else:
	return 1 - ratio

    def ratio(self, deck):
      return 0.0
      
class DeckPercentageTrump(AbstractRatioIteration):
    def ratio(self, deck):
	return self.test(
	  self.config["test"],
	  self.config["ratio"],
	  deck.deck_percentage_trumps(),
	  self.config["value"]
	)

class CountBouts(AbstractRatioIteration):
    def ratio(self, deck):
	return self.test(
	  self.config["test"],
	  self.config["ratio"],
	  deck.count_bouts(),
	  self.config["value"]
	)

class CountFaceIs(AbstractRatioIteration):
    def ratio(self, deck):
	return self.test(
	  self.config["test"],
	  self.config["ratio"],
	  deck.count_face_is(self.config["name"]),
	  self.config["value"]
	)

class CountCuts(AbstractRatioIteration):
    def ratio(self, deck):
	return self.test(
	  self.config["test"],
	  self.config["ratio"],
	  deck.count_cuts(),
	  self.config["value"]
	)

class CountTrumps(AbstractRatioIteration):
  def ratio(self, deck):
      return self.test(
	self.config["test"],
	self.config["ratio"],
	deck.count_trumps(),
	self.config["value"]
      )

class ScoreFaces(AbstractRatioIteration):
    def ratio(self, deck):
	return self.test(
	  self.config["test"],
	  self.config["ratio"],
	  deck.score_faces(),
	  self.config["value"]
	)

class Proba(object):
  def __init__(self):
    self.objects = [
        DeckPercentageTrump({"test": ">=", "value": 33.33, "ratio": 0.8}), # le test ne fonctionne pas comme souhaiter
	CountBouts({"test": ">=", "value": 1, "ratio": 0.8}),
	CountFaceIs({"name": "king", "test": ">=", "value": 2, "ratio": 0.6 }),
	CountCuts({"test": ">=", "value":1, "ratio": 0.6}),
	ScoreFaces({"test": ">=", "value": 20, "ratio": 0.6}),
	CountTrumps({"test": "<=", "value": 3, "ratio": 0.1}),
    ]

  def ratio(self,deck):
    ratio = 1
    for ratio_object in self.objects:
	ratio *= ratio_object.ratio(deck)
    return ratio




proba = Proba()
print "1]", deck1, proba.ratio(deck1)
print "2]", deck2, proba.ratio(deck2)
print "3]", deck3, proba.ratio(deck3)
print "4]", deck4, proba.ratio(deck4)
print "5]", deck5, proba.ratio(deck5)
print "6]", deck6, proba.ratio(deck6)