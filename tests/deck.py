'''
Created on 4 juin 2010

@author: mathgl
'''

from tarot.deck import Deck
from tarot.card import Card, ExcuseCard, TrumpCard, FaceCard

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
              Card("diamonds", 6),
              Card("diamonds", 7),
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
              Card("diamonds", 3), #10
              Card("diamonds", 4),
              Card("diamonds", 6),
              Card("diamonds", 7),
              Card("diamonds", 8),
              Card("diamonds", 10)
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
              Card("diamonds", 3), #10
              Card("diamonds", 4),
              Card("diamonds", 6),
              Card("diamonds", 7),
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
              FaceCard("diamonds", "queen"),
              Card("diamonds", 7),
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
              TrumpCard(11),
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
              Card("diamonds", 10),
              Card("diamonds", 9),
              Card("diamonds", 8),
              Card("hearts", 10),
              Card("hearts", 10),
              Card("spades", 10),
              Card("spades", 9),
              Card("clubs", 10),
])
