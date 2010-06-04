#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tests.deck import deck1, deck2, deck3, deck4, deck5, deck6

from tarot.ai.test.runner import Runner, a_test_list 
print deck1.card_list
proba = Runner(deck1, a_test_list())
print proba.test()
