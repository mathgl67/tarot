#! /usr/bin/env python

'''
Created on 8 juin 2010

@author: mathgl
'''
import sys
from PyQt4 import QtGui
from tarot.ui.window.game import GameWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
