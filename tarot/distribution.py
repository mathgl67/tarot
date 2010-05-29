# !/usr/bin/env python

import random

class Distribution3(object):
    def __init__(self, jeu):
        self.jeu = jeu

    def make_init(self):
        self.premier_tour = True
        self.jeu_reste = len(self.jeu)

        self.joueur_courant = 2
        self.joueurs = [[],[],[]]
        self.joueurs_count = [0,0,0]

        self.chien = []
        self.chien_nombre = 0

    def ajout_carte(self, liste, carte):
        liste.append(carte)
        self.jeu_reste -= 1

    def ajout_chien(self, carte):
        self.ajout_carte(self.chien, carte)
        self.chien_nombre += 1

    def ajout_joueur_numero(self, numero, carte):
        self.ajout_carte(self.joueurs[numero], carte)
        self.joueurs_count[numero] += 1

    def ajout_joueur(self, carte):
        self.ajout_joueur_numero(self.joueur_courant, carte)
        # changement automatique de joueur
        self.joueur_courant -= 1
        if self.joueur_courant < 0:
            self.joueur_courant = 2
            self.premier_tour = False

    def peupas_ajouter_chien(self):
        est_complet = self.chien_nombre is 6
        return est_complet or self.premier_tour
        
    def doit_ajouter_chien(self):
        reste = 6 - self.chien_nombre

        if reste is self.jeu_reste - 3:
            return True

        return False

    def pour_le_chien(self):
        # 1 - je peux ?
        # 2 - je dois ?
        # 3 - je veux ?
        debug = False

        if self.peupas_ajouter_chien():
            if debug:
                print "je peux pas!"
            return False

        if self.doit_ajouter_chien():
            if debug:
                print "je dois!!!!"
            return True

        pif = random.randrange(0,100)
        if pif < 10:
            if debug:
                print "je veux!!!"
            return True
            
        if debug:
            print "je veux pas!!"
        return False

    def make(self):
        self.make_init()

        for carte in self.jeu:
            if self.pour_le_chien():
                self.ajout_chien(carte)
            else:
                self.ajout_joueur(carte)

        return (self.joueurs[0], self.joueurs[1], self.joueurs[2], self.chien)

