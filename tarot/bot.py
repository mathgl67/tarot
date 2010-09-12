
from PyQt4 import QtCore

from tarot.server.client import Client

class Bot(Client):
    
    quitRequested=QtCore.pyqtSignal()
    
    def __init__(self, options):
        Client.__init__(self)
        self.options = options
        
        self.connected.connect(self.connected_)
        
        self.disconnected.connect(self.disconnected_)
        self.channel_message_received.connect(self.channel_message_received_)
        
    def connected_(self):
        self.auth(self.options["user"], self.options["user_password"])
        self.channel_enter(self.options["channel"], self.options["channel_password"])
    
    def disconnected_(self):
        self.quitRequested.emit()
    
    def channel_message_received_(self, user, message):
        if message == "quit":
            self.quitRequested.emit() 