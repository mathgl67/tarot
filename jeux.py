# !/usr/bin/env python

import random
import carte

def generer_couleur(couleur):
    liste = []
    for numero in range(1,11):
        liste.append(carte.Carte(couleur, numero))

    for figure in ["valet", "cavalier", "dame", "roi"]:
        liste.append(carte.Figure(couleur, figure))

    return liste

def generer_atout():
    liste = []
    for numero in range(1,22):
        liste.append(carte.Atout(numero))

    return liste

def generer_jeux():
    liste = []
    liste.extend(generer_couleur("coeur"))
    liste.extend(generer_couleur("trefle"))
    liste.extend(generer_couleur("carreau"))
    liste.extend(generer_couleur("pique"))
    liste.extend(generer_atout())
    liste.append(carte.Excuse())
    return liste

def melanger(jeu):
    random.shuffle(jeu)

