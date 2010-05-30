
from tarot.card import Card, FaceCard, TrumpCard, ExcuseCard

class Deck(object):
	def __init__(self, card_list=None):
		self.card_list = card_list if card_list else []

	def _count_isinstance(self, cls):
		count = 0
		for card in self.card_list:
			if isinstance(card, cls):
				count += 1
		return count

	def count_trumps(self):
		return self._count_isinstance(TrumpCard)

	def count_faces(self):
		return self._count_isinstance(FaceCard)

	def count_bouts(self):
		count = 0
		for card in self.card_list:
			if card.is_bout():
				count += 1
		return count

	def score(self):
		score = 0
		for card in self.card_list:
			score += card.score()
		return score
