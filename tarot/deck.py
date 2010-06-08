# -*- coding: utf-8 -*-

import random

from tarot.card import Card, ExcuseCard, TrumpCard, FaceCard
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

    def append(self, card):
        self.card_list.append(card)

    def shuffle(self):
        random.shuffle(self.card_list)

    def count(self):
        return len(self.card_list)

    def score(self):
        score = 0
        for card in self.card_list:
            score += card.score()
        return score

    def informations(self):
        return DeckInformation(self)
    


class DeckGeneration(object):
    @staticmethod
    def _suit(suit_name):
        suit = []
        for number in range(1, 11):
            suit.append(Card(suit_name, number))
        for face_card in ["jack", "knight", "queen", "king"]:
            suit.append(FaceCard(suit_name, face_card))
        return suit
    
    @staticmethod
    def suit(suit_name):
        return Deck(DeckGeneration._suit(suit_name))

    @staticmethod
    def _trumps():
        trumps = []
        for number in range(1, 22):
            trumps.append(TrumpCard(number))

        return trumps

    @staticmethod
    def trumps():
        return Deck(DeckGeneration._trumps())

    @staticmethod
    def _full():
        tarot_cards = []
        for suit_name in ["diamonds", "clubs", "hearts", "spades"]:
            tarot_cards.extend(DeckGeneration._suit(suit_name))

        tarot_cards.extend(DeckGeneration._trumps())
        tarot_cards.append(ExcuseCard())
    
        return tarot_cards
    
    @staticmethod
    def full():
        return Deck(DeckGeneration._full())