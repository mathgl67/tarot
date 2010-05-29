
from PyQt4 import QtGui, QtCore

from tarot import jeux, distribution
from tarot.ui.generated.generate import Ui_Generateur 

def debug_print(joueur1, joueur2, joueur3, chien):
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

class GenerateWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_Generateur()
		self.ui.setupUi(self)
		# signals
		QtCore.QObject.connect(
			self.ui.Distribution_3J,
			QtCore.SIGNAL("activated()"),
			self.distribution_3j_activated
		)

		QtCore.QObject.connect(
			self.ui.Joueur1,
			QtCore.SIGNAL("clicked()"),
			self.joueur1_clicked
		)

		QtCore.QObject.connect(
			self.ui.Joueur2,
			QtCore.SIGNAL("clicked()"),
			self.joueur2_clicked
		)

		QtCore.QObject.connect(
			self.ui.Joueur3,
			QtCore.SIGNAL("clicked()"),
			self.joueur3_clicked
		)

		QtCore.QObject.connect(
			self.ui.Chien,
			QtCore.SIGNAL("clicked()"),
			self.chien_clicked
		)


	def distribution_3j_activated(self):
		print "Distrib3j activated()"
		jeu = jeux.generer_jeux()
		jeux.melanger(jeu)

		dist = distribution.Distribution3(jeu)
		(self.joueur1, self.joueur2, self.joueur3, self.chien) = dist.make()
		debug_print(self.joueur1, self.joueur2, self.joueur3, self.chien)

		#create scene
		self.scene_j1 = self.create_scene(self.joueur1)
		self.scene_j2 = self.create_scene(self.joueur2)
		self.scene_j3 = self.create_scene(self.joueur3)
		self.scene_ch = self.create_scene(self.chien)

		#set scene to joueur 1
		self.ui.GraphicView.setScene(self.scene_j1)
		

	def create_scene(self, carte_list):
		scene = QtGui.QGraphicsScene(self.ui.GraphicView)
                pix_size = { "width": 155 * 0.5, "height": 220 * 0.5 }
		x = y = 0
                for carte in carte_list:
                        scene.addItem(carte)
                        carte.setPos(x * pix_size["width"], y * pix_size["height"])
			carte.scale(0.5, 0.5)
			# increment
                        x += 1
                        if x is 8:
                                x = 0
				y += 1
		return scene
			

	def joueur1_clicked(self):
		print "Joueur1 clicked()"
                self.ui.GraphicView.setScene(self.scene_j1)

	def joueur2_clicked(self):
		print "Joueur2 clicked()"
                self.ui.GraphicView.setScene(self.scene_j2)

	def joueur3_clicked(self):
		print "Joueur3 clicked()"
                self.ui.GraphicView.setScene(self.scene_j3)

	def chien_clicked(self):
		print "chien clicked()"
                self.ui.GraphicView.setScene(self.scene_ch)






