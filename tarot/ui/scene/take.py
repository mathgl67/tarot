'''
Created on 13 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui

class TakeScene(QtGui.QGraphicsScene):
    def __init__(self, contract, parent=None):
        super(TakeScene, self).__init__(parent)
        
        