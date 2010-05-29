
from PyQt4 import QtGui, QtCore

from tarot import jeux, distribution
from tarot.ui.generated.generate import Ui_Generator

def debug_print(player_dict, dog):
	for num, player in player_dict.iteritems():
		print "Player %d:" % (num+1)
		for card in player:
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
			self.ui.Distribute_3P,
			QtCore.SIGNAL("activated()"),
			self.distribute_3p_activated
		)

		QtCore.QObject.connect(
			self.ui.PlayerPrev,
			QtCore.SIGNAL("clicked()"),
			self.player_prev_clicked
		)

		QtCore.QObject.connect(
			self.ui.Players,
			QtCore.SIGNAL("clicked()"),
			self.players_clicked
		)

		QtCore.QObject.connect(
			self.ui.PlayerNext,
			QtCore.SIGNAL("clicked()"),
			self.player_next_clicked
		)

		QtCore.QObject.connect(
			self.ui.Dog,
			QtCore.SIGNAL("clicked()"),
			self.dog_clicked
		)


	def distribute_3p_activated(self):
		print "Distribute 3p activated()"
		jeu = jeux.generer_jeux()
		jeux.melanger(jeu)

		dist = distribution.Distribution3(jeu)
		self.player_list = {} 
		(self.player_list[0],
		 self.player_list[1],
		 self.player_list[2],
                 self.dog) = dist.make()
		debug_print(self.player_list, self.dog)

		#create scenes
		self.scene_list = {}
		for num, player in self.player_list.iteritems():
			self.scene_list[num] = self.create_scene(player)

		self.scene_dog = self.create_scene(self.dog)

		#set scene to player 1
		self.ui.GraphicView.setScene(self.scene_list[0])
		self.number_of_player = 3
		self.current_player = 0
		
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
			
	def display_player_scene(self):
		scene = self.scene_list[self.current_player]
                self.ui.GraphicView.setScene(scene)

	def player_prev_clicked(self):
		print "Player Previous clicked()"
		if self.current_player > 0:
			self.current_player -= 1
		self.display_player_scene()

	def players_clicked(self):
		print "Players clicked()"
		self.display_player_scene()

	def player_next_clicked(self):
		print "Player Next clicked()"
		if self.current_player + 1 < self.number_of_player:
			self.current_player += 1
		self.display_player_scene()

	def dog_clicked(self):
		print "Dog clicked()"
                self.ui.GraphicView.setScene(self.scene_dog)

