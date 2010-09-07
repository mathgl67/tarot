'''
Created on 8 juin 2010

@author: mathgl
'''

from PyQt4 import QtGui, QtNetwork
from PyQt4.QtCore import Qt

from tarot.ui.generated.game import Ui_GameWindow
from tarot.ui.window.new_connection import ConnectionDialog
from tarot.server.message import Message
from tarot.server.client import Client

class ChatWidget(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.webView = self.main_window.ui.webViewChat
        self.lineEdit = self.main_window.ui.lineEditChat
        self.lineEdit.returnPressed.connect(self.send_message)
        
        self.css = """
            .notice {
                font-size: 9pt;
                color: gray;
            }
            
            .notice:before {
                content: " --- ";
            }
           
            .author {
                color: red;
            }
            
            .author:before {
                content: "<"
            }
            
            .author:after {
                content: "> ";
            }
            
            .message {
                font-size: 10pt;
            }
        """
        self.frame = """
        <html>
        <head>
            <style type="text/css">
            %s
            </style>
        </head>
        <body>
            %s
        </body>
        </html>
        """
              
        self.content = ""
    
    def update(self):
        self.webView.setHtml(self.frame % (
            self.css,
            self.content
        )) 
        self.webView.page().mainFrame().setScrollBarValue(Qt.Vertical, self.webView.page().mainFrame().scrollBarMaximum(Qt.Vertical))
        
         
    def notice(self, text):
        self.content += """
            <div class="notice">
                %s
            </div>""" % text
        self.update()      
        
    def message(self, author, text):
        self.content += """
            <div class="message">
                <span class="author">%s</span>
                <span class="text">%s</span>
            </div>
        """ % (
            author,
            text
        )
        self.update()

    def send_message(self):
        message = self.lineEdit.text()
        self.lineEdit.clear()
        print "should send:", message
        if self.main_window.socket:
            self.main_window.socket.write(
                """<channel-message message="%s" />\n""" % (message)
            )
            

class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.socket = Client()
        self.socket.connected.connect(self.connected)
        self.socket.channel_message_received.connect(self.channel_message_received)
        self.socket.channel_join_received.connect(self.channel_join_received)
        self.socket.channel_left_received.connect(self.channel_left_received)
        self.socket.channel_users_received.connect(self.channel_users_received)
        
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
 
        self.ui.actionConnection.triggered.connect(self.connection)
        self.chat_widget = ChatWidget(self)
                 
    def connection(self):
        dialog = ConnectionDialog()
        if dialog.exec_():
            self.connection_opts = dialog.get_result()
            self.socket.connectToHost(
                self.connection_opts["host"],
                self.connection_opts["port"]
            )
    
    def connected(self):
            self.socket.auth(
                self.connection_opts["user"],
                self.connection_opts["user_password"]
            )
            self.socket.channel_enter(
                self.connection_opts["channel"],
                self.connection_opts["channel_password"]
            )

    def channel_join_received(self, user):
        self.chat_widget.notice("%s enter." % user)
        print "ask channel users update"
        self.socket.channel_users()

    def channel_left_received(self, user):
        self.chat_widget.notice("%s left." % user)
        print "ask channel users update"
        self.socket.channel_users()

    def channel_message_received(self, user, message):
        self.chat_widget.message(user, message) 
    
    def channel_users_received(self, user_list):
        self.ui.listWidgetUsers.clear()
        for user in user_list:
            self.ui.listWidgetUsers.addItem(user)
