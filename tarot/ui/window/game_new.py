'''
Created on 8 juin 2010

@author: mathgl
'''

from tarot.game import Game
from tarot.player import GuiPlayer
from tarot.ai.player import DummyAiPlayer

from PyQt4 import QtGui
from tarot.ui.generated.new_game_dialog import Ui_NewGameDialog

class NewGameDialog(QtGui.QDialog):
    def __init__(self):
        super(NewGameDialog, self).__init__()
        self.ui = Ui_NewGameDialog()
        self.ui.setupUi(self)

    def get_result(self):
        game = Game(self.ui.numberOfPlayer.value())
        game.player_list.append(GuiPlayer("mathgl"))
        for num in range(0, self.ui.numberOfAi.value()):
            game.player_list.append(DummyAiPlayer("ai_%d" % num))
        
        return game