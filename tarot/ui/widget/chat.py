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
    def __init__(self, main_window):
        QtCore.QObject.__init__(self)
        
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
        if self.main_window.socket:
            self.main_window.stream.output.channel_message(message)
            
