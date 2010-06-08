# -*- coding: utf-8 -*-

import random

from tarot.deck import Deck

class Distribute(object):
    def __init__(self, deck, player_count):
        self.deck = deck
        self.player_count = player_count
        if self.player_count is 5:
            self.dog_full_count = 3
        else:
            self.dog_full_count = 6

    def init(self):
        self.first_round = True
        self.card_count_left = self.deck.count()

        self.current_player = self.player_count - 1
        self.player_list = {}
         
        for num in range(0, self.player_count):
            self.player_list[num] = Deck()

        self.dog = Deck()
        self.dog_count = 0

    def add_card(self, deck, card):
        deck.append(card)
        self.card_count_left -= 1

    def add_dog(self, card):
        self.add_card(self.dog, card)
        self.dog_count += 1

    def add_player_num(self, num, card):
        self.add_card(self.player_list[num], card)

    def add_player(self, card):
        self.add_player_num(self.current_player, card)
        # auto changing current_player
        self.current_player -= 1
        if self.current_player < 0:
            self.current_player = self.player_count - 1 
            self.first_round = False

    def i_cant_add_in_dog(self):
        is_full = self.dog_count is self.dog_full_count
        return is_full or self.first_round
        
    def i_must_add_in_dog(self):
        left = self.dog_full_count - self.dog_count

        if left is self.card_count_left - self.player_count:
            return True

        return False

    def decide_for_the_dog(self):
        # 1 - can ?
        # 2 - must ?
        # 3 - want ?
        debug = False

        if self.i_cant_add_in_dog():
            if debug:
                print "I can't add card in the dog."
            return False

        if self.i_must_add_in_dog():
            if debug:
                print "I must add card in the dog."
            return True

        pif = random.randrange(0, 100)
        if pif < 10:
            if debug:
                print "I want add card in the dog."
            return True
            
        if debug:
            print "I don't want to add card in the dog."
        return False

    def do(self):
        self.init()

        for card in self.deck.card_list:
            if self.decide_for_the_dog():
                self.add_dog(card)
            else:
                self.add_player(card)

        return (self.player_list, self.dog)
