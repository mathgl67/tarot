#! /usr/bin/env python

class CarteAbstraite(object):
    def __init__(self):
        pass

class Couleur(CarteAbstraite):
    def __init__(self, couleur):
        CarteAbstraite.__init__(self)
        self.couleur = couleur

    def __repr__(self):
        return "couleur=%s" % (self.couleur)

class Numero(CarteAbstraite):
    def __init__(self, numero):
        CarteAbstraite.__init__(self)
        self.numero = numero

    def __repr__(self):
        return "numero=%s" % (self.numero)

class Carte(Couleur, Numero):
    def __init__(self, couleur, numero):
        Couleur.__init__(self, couleur)
        Numero.__init__(self, numero)

    def __repr__(self):
        return "Carte(%s,%s)" % (
            Couleur.__repr__(self),
            Numero.__repr__(self)
        )

class Figure(Couleur):
    def __init__(self, couleur, figure):
        Couleur.__init__(self, couleur)
        self.figure = figure

    def __repr__(self):
        return "Figure(%s,figure=%s)" % (
            Couleur.__repr__(self),
            self.figure
        )

class Atout(Numero):
    def __repr__(self):
        return "Atout(%s)" % (Numero.__repr__(self))

class Excuse(CarteAbstraite):
    def __init__(self):
        pass

    def __repr__(self):
        return "Excuse()"
