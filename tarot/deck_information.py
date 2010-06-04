# -*- coding: utf-8 -*-

from tarot.card import Card, FaceCard, TrumpCard

class DeckInformation(object):
    def __init__(self, deck):
        self.deck = deck
        
    def _count_isinstance(self, cls):
        count = 0
        for card in self.deck.card_list:
            if isinstance(card, cls):
                count += 1
        return count

    def deck_percentage_trumps(self):
        return float(100 * self.count_trumps()) / self.deck.count()

    def deck_percentage_faces(self):
        return float(100 * self.count_faces()) / self.deck.count()

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
        for card in self.deck.card_list:
            if isinstance(card, FaceCard) and card.name == face:
                count += 1
        return count

    def count_bouts(self):
        count = 0
        for card in self.deck.card_list:
            if card.is_bout():
                count += 1
        return count

    def count_cuts(self):
        count_tab = {
            "hearts": 0,
            "clubs": 0,
            "diamonds": 0,
            "spades": 0,
        }
        for card in self.deck.card_list:
            if isinstance(card, FaceCard) or isinstance(card, Card):
                count_tab[card.suit] += 1
        
        count_cut = 0
        for count in count_tab.itervalues():
            if count == 0:
                count_cut += 1
          
        return count_cut

    def score_faces(self):
        score = 0
        for card in self.deck.card_list:
            if isinstance(card, FaceCard):
                score += card.score()
        return score
