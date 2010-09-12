
from PyQt4 import QtCore, QtNetwork, QtXml
from tarot.server.message import Message

class Client(QtNetwork.QTcpSocket):
    channel_join_received = QtCore.pyqtSignal(str)
    channel_left_received = QtCore.pyqtSignal(str)
    channel_users_received = QtCore.pyqtSignal(list)
    channel_message_received = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        QtNetwork.QTcpSocket.__init__(self)
        self.readyRead.connect(self.ready_read)
    
    def send_line(self, line):
        self.write("%s\n" % line)
        
    def auth(self, user, password):
        self.send_line(Message.simple("auth", {
           "user": user,
           "password": password 
        }))
        
    def channel_enter(self, name, password):
        self.send_line(Message.simple("channel-enter", {
            "name": name,
            "password": password
        }))
        
    def channel_message(self, message):
        self.send_line(Message.simple("channel-message", {
            "message": message
        }))
    
    def channel_users(self):    
        self.send_line(Message.simple("channel-users"))
    
    def game_start(self, user_list):
        self.send_line(Message.game_start(user_list))
    
    def ready_read(self):
        line = self.readLine()
        if not line:
            return
                        
        print "receive:", line[:-1]
        document = QtXml.QDomDocument()     
        (ret, error_msg, error_line, error_column) = document.setContent(line)
        if not ret:
            print "parse:", line 
            print "error:", error_msg, "(line=", error_line, ";column=", error_column, ")"
            return
        
        root = document.documentElement()
        print "roottag:", root.tagName()
        
        if root.tagName() == "channel-message":
            user = root.attribute("user")
            message = root.attribute("message")
            self.channel_message_received.emit(user, message)
        elif root.tagName() == "channel-join":
            user = root.attribute("user")
            self.channel_join_received.emit(user)
        elif root.tagName() == "channel-left":
            user = root.attribute("user")
            self.channel_left_received.emit(user)
        elif root.tagName() == "channel-users":
            node = root.firstChild()
            user_list = []
            while not node.isNull():
                if node.isElement():
                    elem = node.toElement()
                    if elem.tagName() == "user":
                        user_list.append(elem.attribute("name"))
                self.channel_users_received.emit(user_list)
                node = node.nextSibling()
        
        # recurse until end of data    
        self.ready_read()                