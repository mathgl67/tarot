
from PyQt4 import QtCore

class ChatWidget(QtCore.QObject):
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
        message = self.lineEdit.text()
        self.lineEdit.clear()
        print "should send:", message
        if self.main_window.socket:
            self.main_window.socket.write(
                """<channel-message message="%s" />\n""" % (message)
            )
            
