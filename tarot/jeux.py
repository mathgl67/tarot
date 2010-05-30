# !/usr/bin/env python

import random
from tarot.card import Card, FaceCard, TrumpCard, ExcuseCard

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

