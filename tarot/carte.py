#! /usr/bin/env python

from PyQt4 import QtGui

class CarteAbstraite(QtGui.QGraphicsPixmapItem):
    def __init__(self):
	super(CarteAbstraite, self).__init__()
	self.setPixmap(self._get_pixmap())

    def _get_pixmap(self):
	return QtGui.QPixmap("images/vide.png")

class Carte(CarteAbstraite):
    def __init__(self, couleur, numero):
	self.couleur = couleur
	self.numero = numero
	super(Carte, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap(
		"images/cartes/%s/%d.png" % (self.couleur, self.numero)
	)

    def __repr__(self):
        return "Carte(couleur=%s,numero=%s)" % (
            self.couleur,
            self.numero
        )

class Figure(CarteAbstraite):
    def __init__(self, couleur, figure):
	self.couleur = couleur
        self.figure = figure
        super(Figure, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap(
		"images/cartes/%s/%s.png" % (self.couleur, self.figure)
	)

    def __repr__(self):
        return "Figure(couleur=%s,figure=%s)" % (
	    self.couleur,
            self.figure
        )

class Atout(CarteAbstraite):
    def __init__(self, numero):
	self.numero = numero
	super(Atout, self).__init__()

    def _get_pixmap(self):
	return QtGui.QPixmap("images/cartes/atous/%d.png" % self.numero)

    def __repr__(self):
        return "Atout(numero=%s)" % self.numero

class Excuse(CarteAbstraite):
    def _get_pixmap(self):
	return QtGui.QPixmap("images/cartes/atous/excuse.png")

    def __repr__(self):
        return "Excuse()"
