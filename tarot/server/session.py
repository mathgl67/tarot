
from PyQt4 import QtCore, QtXml

class Session(QtCore.QThread):
    def __init__(self, server, client):
        QtCore.QThread.__init__(self)
        self.server = server
        self.server.session_list.append(self)
        self.socket = client
        self.socket.readyRead.connect(self.socket_ready_read)
        self.socket.disconnected.connect(self.socket_disconnected)
        self.user = None
        self.channel = None
    
    def new_xml(self, element_name):
        doc = QtXml.QDomDocument()
        elem = doc.createElement(element_name)
        doc.appendChild(elem)
        return (doc, elem)
    
    def send_xml(self, document):
        data = document.toString()
        data.replace("\n", "") # This is bad...
        self.socket.write("%s\n" % data)         
    
    def socket_disconnected(self):
        print "disconnected"
        if self.channel:
            # leave the channel
            (leave_doc, leave) = self.new_xml("channel-left")
            leave.setAttribute("user", self.user.name)
            self.server.session_list.send_to_channel(self.channel, leave_doc)
        # stop loop
        self.exit()
        self.wait()
        # remove itself
        self.server.session_list.remove(self)
            
    def socket_line_received(self, line):
        print "line received: %s (%s, %s)" % (line, self.user, self.channel)
        self.server.command_list.run(self, line)
    
    def socket_ready_read(self):
        while True:
            line = self.socket.readLine()
            if not line:
                return
            self.socket_line_received(line)
            
    def run(self):
        """
        This simply execute a loop for the client thread
        """
        self.exec_()

class SessionList(list):
    def user_exists(self, user):
        for session in self:
            if session.user == user:
                return True
        return False
    
    def get_by_channel(self, channel):
        result = SessionList()
        for session in self:
            if session.channel == channel:
                result.append(session)
        return result
    
    def send_to_channel(self, channel, document):
        for session in self.get_by_channel(channel):
            session.send_xml(document)

    def send_to_all(self, document):
        for session in self:
            session.send_xml(document)