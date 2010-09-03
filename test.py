#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tarot.player import PlayerList, AbstractPlayer

p1 = AbstractPlayer("p1")
p2 = AbstractPlayer("p2")
p3 = AbstractPlayer("p3")
p4 = AbstractPlayer("p4")
p5 = AbstractPlayer("p5")


pl = PlayerList()
pl.append(p1)
pl.append(p2)
pl.append(p3)
pl.append(p4)

print pl.getDistributer()

pl.reorder(p3)

print pl.getDistributer()

pl.reorder(p2)

print pl.getDistributer()

pl.reorder(p4)

print pl.getDistributer()
print pl.getDistributer()

print pl.getDistributer()


