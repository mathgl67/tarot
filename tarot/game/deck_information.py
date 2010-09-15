#
# -*- coding: utf8 -*-
#
# Tarot 
# Copyright (C) 2009-2010  mathgl67@gmail.com
#
#  This file is part of Tarot
#
#  Tarot is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Tarot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Tarot.  If not, see <http://www.gnu.org/licenses/>.
#

from tarot.game.card import Card, FaceCard, TrumpCard, ExcuseCard

class DeckInformation(object):
    def __init__(self, deck):
        self.deck = deck
        
    def _count_isinstance(self, cls):
        count = 0
        for card in self.deck.card_list:
            if isinstance(card, cls):
                count += 1
        return count

    def have_bout_name(self, name):
        if name == "excuse":
            if self._count_isinstance(ExcuseCard):
                return True
        
        for card in self.deck.card_list:
            if isinstance(card, TrumpCard):
                if card.number == 1 and name == "1":
                    return True
                elif card.number == 21 and name == "21":
                    return True
                
        return False

    def have_face_suite(self, suit):
        count = 0
        for card in self.deck.card_list:
            if not isinstance(card, FaceCard):
                continue
            if not card.suit == suit:
                continue
            count += 1
        
        if count == 4:
            return True
        return False            

    def count_trump_sup(self, number):
        count = 0
        for card in self.deck.card_list:
            if isinstance(card, TrumpCard):
                if card.number > number:
                    print "card!"
                    count += 1
        print "trump sup:", count
        return count

    def count_face_suite(self):
        count = 0
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            if self.have_face_suite(suit):
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
