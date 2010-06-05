'''
Created on 5 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui
from tarot.ui.generated.ia_taker import Ui_IATaker

class IATakerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IATakerWindow, self).__init__()
        self.ui = Ui_IATaker()
        self.ui.setupUi(self)