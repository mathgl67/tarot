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

from PyQt4 import QtCore

class ChatWidget(QtCore.QObject):
    def __init__(self, window):
        QtCore.QObject.__init__(self)
        
        self.window = window
        self.stream = self.window.stream
        self.webView = self.window.ui.webViewChat
        self.lineEdit = self.window.ui.lineEditChat
        self.lineEdit.returnPressed.connect(self.send_message)
        
        self.stream.input.channel_message_received.connect(self.message)
        self.stream.input.channel_join_received.connect(self.user_join)
        self.stream.input.channel_left_received.connect(self.user_left)
        
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
        self.webView.page().mainFrame().setScrollBarValue(QtCore.Qt.Vertical, self.webView.page().mainFrame().scrollBarMaximum(QtCore.Qt.Vertical))
        
         
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
        print "should message.."
        message = self.lineEdit.text()
        self.lineEdit.clear()
        print "should send:", message
        if self.window.socket:
            self.stream.output.channel_message(message)
            

    def user_join(self, user):
        self.notice("%s enter." % user)
        print "ask channel users update"
        self.stream.output.channel_users()

    def user_left(self, user):
        self.notice("%s left." % user)
        print "ask channel users update"
        self.stream.output.channel_users()
