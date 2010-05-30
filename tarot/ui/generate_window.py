
from PyQt4 import QtGui, QtCore

import tarot.card
from tarot.distribute import Distribute
from tarot.deck import Deck
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
			self.ui.Distribute_4P,
			QtCore.SIGNAL("activated()"),
			self.distribute_4p_activated
		)

		QtCore.QObject.connect(
			self.ui.Distribute_5P,
			QtCore.SIGNAL("activated()"),
			self.distribute_5p_activated
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

	def distribute(self, player_count):
		card_list = tarot.card.generate_tarot_cards()
		tarot.card.shuffle_cards(card_list)

		distribute = Distribute(card_list, player_count)
 
		(self.player_list, self.dog) = distribute.do()
		debug_print(self.player_list, self.dog)

		#create scenes
		self.scene_list = {}
		for num, card_list in self.player_list.iteritems():
			self.scene_list[num] = self.create_scene(
				"Player %d" % (num+1),
				card_list
			)

		self.scene_dog = self.create_scene("Dog", self.dog)

		#set scene to player 1
		self.ui.GraphicView.setScene(self.scene_list[0])
		self.number_of_player = player_count 
		self.current_player = 0

	def distribute_3p_activated(self):
		print "Distribute for 3 players..."
		self.distribute(3)

	def distribute_4p_activated(self):
		print "Distribute for 4 players..."
		self.distribute(4)

	def distribute_5p_activated(self):
		print "Distribute for 5 players..."
		self.distribute(5)
	
	def create_scene(self, title, card_list):
		deck = Deck(card_list) 
		scene = QtGui.QGraphicsScene(self.ui.GraphicView)
                pix_size = { "width": 221 * 0.35, "height": 391 * 0.35 }
		x = y = 0
		# add title on scene
		itm_title = scene.addText(title, QtGui.QFont("Helvsetica", 24)) 
		# add information
		info1 = "Score: %.1f points - Bouts: %d/3" % (
			deck.score(),
			deck.count_bouts()
		)
		itm_info1 = scene.addText(info1, QtGui.QFont("Helvsetica", 12))
		itm_info1.setPos(0, 37)

		info2 = "%d trumps (%.2f%% of hand, %.2f%% of game)" % (
			deck.count_trumps(),
			deck.deck_percentage_trumps(),
			deck.game_percentage_trumps()
		)
		itm_info2 = scene.addText(info2, QtGui.QFont("Helvsetica", 12))
		itm_info2.setPos(0, 51)

		info3 = "%d faces (%.2f%% of hand, %.2f%% of game)" % (
			deck.count_faces(),
			deck.deck_percentage_faces(),
			deck.game_percentage_trumps()
		)
		itm_info3 = scene.addText(info3, QtGui.QFont("Helvsetica", 12))
		itm_info3.setPos(0, 65)

		# place cards on scene
                for card in card_list:
                        card.setPos(x * pix_size["width"], 90 + y * pix_size["height"])
			card.scale(0.35, 0.35)
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

