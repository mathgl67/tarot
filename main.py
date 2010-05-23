#! /usr/bin/env python

import jeux
import distribution

jeu = jeux.generer_jeux()
jeux.melanger(jeu)

distribution = distribution.Distribution3(jeu)
(joueur1, joueur2, joueur3, chien) = distribution.make()

print "jeux generer"
print
print "nombre de carte:", len(jeu)
print
print "joueur1:"
for carte in joueur1:
    print carte
print
print "joueur2:"
for carte in joueur2:
    print carte
print
print "joueur3:"
for carte in joueur3:
    print carte
print
print "chien:"
for carte in chien:
    print carte
