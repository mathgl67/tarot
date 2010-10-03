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

from tarot.stream.server import ServerStream

class Session(QtCore.QThread):
    def __init__(self, server, client):
        QtCore.QThread.__init__(self)
        self.server = server
        self.server.session_list.append(self)
        self.socket = client
        self.socket.disconnected.connect(self.socket_disconnected)
        self.stream = ServerStream(self.socket, self)
        self.stream.output.start()
        self.user = None
        self.channel = None
        self.game = None
    
    def socket_disconnected(self):
        print "disconnected"
        if self.channel:
            # leave the channel
            self.stream.output_channel.base("channel-left", {"user": self.user.name})
            
        # stop loop
        self.exit()
        self.wait()
        # remove itself
        self.server.session_list.remove(self)
             
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
