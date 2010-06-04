#! /usr/bin/env python

from PyQt4 import QtGui
from tarot.ui.window.generate import GenerateWindow

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	window = GenerateWindow()
	window.show()
	sys.exit(app.exec_())
