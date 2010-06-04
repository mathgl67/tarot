# -*- coding: utf-8 -*-

from tarot.deck_information import DeckInformation

class Deck(object):
    """
    This is represent a deck.
    
    :param card_list: the list of card present in the deck.
    :type card_list: list
    """
    def __init__(self, card_list=None):
        self.card_list = card_list if card_list else []

    def __repr__(self):
        return "Deck(count=%d, score=%.1f)" % (self.count(), self.score())

    def count(self):
        return len(self.card_list)

    def score(self):
        score = 0
        for card in self.card_list:
            score += card.score()
        return score

    def informations(self):
        return DeckInformation(self)
    
