#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 5 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui
from tarot.ui.window.ia_taker import IATakerWindow

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = IATakerWindow()
    window.show()
    sys.exit(app.exec_())
