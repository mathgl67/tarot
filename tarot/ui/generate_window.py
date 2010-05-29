
from PyQt4 import QtGui, QtCore

from tarot import jeux, distribution
from tarot.ui.generated.generate import Ui_Generator

def debug_print(p1, p2, p3, dog):
	print "Player 1:"
	for card in p1:
	    print card
	print
	print "Player 2:"
	for card in p2:
	    print card
	print
	print "Player 3:"
	for card in p3:
	    print card
	print
	print "Dog:"
	for card in dog:
	    print card

class GenerateWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_Generator()
		self.ui.setupUi(self)
		# signals
		QtCore.QObject.connect(
			self.ui.Distribution_3P,
			QtCore.SIGNAL("activated()"),
			self.distribution_3p_activated
		)

		QtCore.QObject.connect(
			self.ui.Player1,
			QtCore.SIGNAL("clicked()"),
			self.player1_clicked
		)

		QtCore.QObject.connect(
			self.ui.Player2,
			QtCore.SIGNAL("clicked()"),
			self.player2_clicked
		)

		QtCore.QObject.connect(
			self.ui.Player3,
			QtCore.SIGNAL("clicked()"),
			self.player3_clicked
		)

		QtCore.QObject.connect(
			self.ui.Dog,
			QtCore.SIGNAL("clicked()"),
			self.dog_clicked
		)


	def distribution_3p_activated(self):
		print "Distribution 3p activated()"
		jeu = jeux.generer_jeux()
		jeux.melanger(jeu)

		dist = distribution.Distribution3(jeu)
		(self.p1, self.p2, self.p3, self.dog) = dist.make()
		debug_print(self.p1, self.p2, self.p3, self.dog)

		#create scene
		self.scene_p1 = self.create_scene(self.p1)
		self.scene_p2 = self.create_scene(self.p2)
		self.scene_p3 = self.create_scene(self.p3)
		self.scene_dog = self.create_scene(self.dog)

		#set scene to joueur 1
		self.ui.GraphicView.setScene(self.scene_p1)
		

	def create_scene(self, card_list):
		scene = QtGui.QGraphicsScene(self.ui.GraphicView)
                pix_size = { "width": 155 * 0.5, "height": 220 * 0.5 }
		x = y = 0
                for card in card_list:
                        card.setPos(x * pix_size["width"], y * pix_size["height"])
			card.scale(0.5, 0.5)
                        scene.addItem(card)
			# increment
                        x += 1
                        if x is 8:
                                x = 0
				y += 1
		return scene
			

	def player1_clicked(self):
		print "Player 1 clicked()"
                self.ui.GraphicView.setScene(self.scene_p1)

	def player2_clicked(self):
		print "Player 2 clicked()"
                self.ui.GraphicView.setScene(self.scene_p2)

	def player3_clicked(self):
		print "Player 3 clicked()"
                self.ui.GraphicView.setScene(self.scene_p3)

	def dog_clicked(self):
		print "dog clicked()"
                self.ui.GraphicView.setScene(self.scene_dog)

