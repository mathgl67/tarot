
from PyQt4 import QtGui, QtCore

import os.path

from tarot.deck import DeckGeneration
from tarot.distribute import Distribute

from tarot.ui.image.store import ImageStore
from tarot.ui.scene.hand import HandScene
from tarot.ui.generated.generate import Ui_Generator

from tarot.ai.take import Take

def debug_print(player_dict, dog):
    for num, deck in player_dict.iteritems():
        print "Player %d:" % (num + 1)
        for card in deck.card_list:
            print card
    print
    print "Dog:"
    for card in dog.card_list:
        print card

class GenerateWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_Generator()
        self.ui.setupUi(self)
        self.take = None
        self.image_store = ImageStore(os.path.join("images", "cards"))
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
        deck = DeckGeneration.full()
        deck.shuffle()

        distribute = Distribute(deck, player_count)
 
        (self.player_list, self.dog) = distribute.do()
        debug_print(self.player_list, self.dog)

        #set ia take
        self.take = Take("test", player_count)

        #create scenes
        self.scene_list = {}
        for num, deck in self.player_list.iteritems():
            self.scene_list[num] = HandScene(
                "Player %d (AI: %s)" % (num + 1, self.take.take(deck)),
                deck,
                self.image_store,
                self.ui.GraphicView
            )

        self.scene_dog = HandScene("Dog", self.dog, self.image_store, self.ui.GraphicView)

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
