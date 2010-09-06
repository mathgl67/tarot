
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
