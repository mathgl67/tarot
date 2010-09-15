#
# -*- coding: utf8 -*-
#
# Tarot 
# Copyright (C) 2009-2010  mathgl67@gmail.com
#
#  This file is part of Tarot
#
#  Tarot is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Tarot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Tarot.  If not, see <http://www.gnu.org/licenses/>.
#

from PyQt4 import QtGui

from tarot.ui.generated.new_connection import Ui_ConnectionDialog

class ConnectionDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)
        
    def get_result(self):
        return {
            "host": self.ui.lineEditHost.text(),
            "port": int(self.ui.lineEditPort.text()),
            "user": self.ui.lineEditUser.text(),
            "user_password": self.ui.lineEditUserPassword.text(),
            "channel": self.ui.lineEditChannel.text(),
            "channel_password": self.ui.lineEditChannelPassword.text(),
        }
