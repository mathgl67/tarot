# -*- coding: utf-8 -*-

from tarot.card import Card, FaceCard, TrumpCard, ExcuseCard

class Deck(object):
	def __init__(self, card_list=None):
		self.card_list = card_list if card_list else []

	def __repr__(self):
	  return "Deck(bouts=%d, trumps=%d, kings=%d, cuts=%d, score_faces=%d)" % (
	    self.count_bouts(),
	    self.count_trumps(),
	    self.count_face_is("king"),
	    self.count_cuts(),
	    self.score_faces()
	  )

	def _count_isinstance(self, cls):
		count = 0
		for card in self.card_list:
			if isinstance(card, cls):
				count += 1
		return count

	def deck_percentage_trumps(self):
		return float(100 * self.count_trumps()) / len(self.card_list)

	def deck_percentage_faces(self):
		return float(100 * self.count_faces()) / len(self.card_list)

	def game_percentage_trumps(self):
		return float(100 * self.count_trumps()) / 21 

	def game_percentage_faces(self):
		return float(100 * self.count_faces()) / 16

	def count_trumps(self):
		return self._count_isinstance(TrumpCard)

	def count_faces(self):
		return self._count_isinstance(FaceCard)

	def count_face_is(self, face):
		count = 0
		for card in self.card_list:
		    if isinstance(card, FaceCard):
			if card.name == face:
			    count += 1
		return count

	def count_bouts(self):
		count = 0
		for card in self.card_list:
			if card.is_bout():
				count += 1
		return count

	def count_cuts(self):
		count_tab = {
		    "hearts": 0,
		    "clubs": 0,
		    "diamons": 0,
		    "spades": 0,
		}
		for card in self.card_list:
		      if isinstance(card, FaceCard) or isinstance(card, Card):
			  count_tab[card.suit] += 1
		
		count_cut = 0
		for count in count_tab.itervalues():
		    if count == 0:
		      count_cut += 1
	      
		return count_cut

	def score(self):
		score = 0
		for card in self.card_list:
			score += card.score()
		return score

	def score_faces(self):
	    score = 0
	    for card in self.card_list:
		if isinstance(card, FaceCard):
		  score += card.score()
	    return score