
from tarot.server.session import SessionList, Session
from tarot.server.command import CommandList

from PyQt4 import QtCore, QtNetwork

class TcpServer(QtNetwork.QTcpServer):
    def __init__(self, application, config_store):
        QtNetwork.QTcpServer.__init__(self)
        self.application = application
        self.newConnection.connect(self.new_connection)
        
        self.thread_pool = QtCore.QThreadPool.globalInstance()
        self.config_store = config_store
        self.session_list = SessionList()
        self.command_list = CommandList()
            
    def listen(self):
        if self.config_store.host:
            host = QtNetwork.QHostAddress()
            host.setAddress(self.config_store.host)
        
        return QtNetwork.QTcpServer.listen(
            self,
            host, #(self.config_store.host),
            self.config_store.port
        )
    
    def new_connection(self):
        print "new connection: add to session list"
        client = self.nextPendingConnection()
        session = Session(self, client)
        session.start()
