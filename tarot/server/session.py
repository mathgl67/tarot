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

from tarot.server.message import Message

class Session(QtCore.QThread):
    def __init__(self, server, client):
        QtCore.QThread.__init__(self)
        self.server = server
        self.server.session_list.append(self)
        self.socket = client
        self.socket.readyRead.connect(self.socket_ready_read)
        self.socket.disconnected.connect(self.socket_disconnected)
        self.reader = QtCore.QXmlStreamReader()
        self.user = None
        self.channel = None
        self.deck = None
    
    def send_line(self, line):
        self.socket.write("%s\n" % line)
    
    def socket_disconnected(self):
        print "disconnected"
        if self.channel:
            # leave the channel
            self.server.session_list.send_to_channel(self.channel,
                Message.simple("channel-left", {"user": self.user.name})
            )
            
        # stop loop
        self.exit()
        self.wait()
        # remove itself
        self.server.session_list.remove(self)
            
    def socket_line_received(self, line):
        print "line received: %s (%s, %s)" % (line, self.user, self.channel)
        self.server.command_list.run(self, line)
    
    def socket_ready_read(self):
        content = self.socket.readAll()
        print "content:", content
        self.reader.addData(content)
        
        while not self.reader.atEnd():
            self.reader.readNext()
            if self.reader.hasError():
                if self.reader.error() == QtCore.QXmlStreamReader.PrematureEndOfDocumentError:
                    print "document not finish.."
                else:
                    print "document error:", self.reader.errorString()
                    self.reader.clear()
            else:
                if self.reader.isStartDocument():
                    print "document start"
                    continue
                elif self.reader.isEndDocument():
                    print "document end: closing socket"
                    self.socket.close()
                elif self.reader.isEndElement():
                    print "document element ended..."
                elif self.reader.isStartElement():
                    print "document element start"
                    if not self.reader.name().toString() == "stream":
                        self.server.command_list.run(self)
            
    def run(self):
        """
        This simply execute a loop for the client thread
        """
        self.exec_()

class SessionList(list):
    def user_exists(self, user):
        if self.get_by_user_name(user.name):
            return True 
        return False
    
    def get_by_user_name(self, user_name):
        for session in self:
            if session.user and session.user.name == user_name:
                return session
        
        return None
    
    def get_by_channel(self, channel):
        result = SessionList()
        for session in self:
            if session.channel == channel:
                result.append(session)
        return result
    
    def send_to_channel(self, channel, line):
        for session in self.get_by_channel(channel):
            session.send_line(line)

    def send_to_all(self, line):
        for session in self:
            session.send_line(line)