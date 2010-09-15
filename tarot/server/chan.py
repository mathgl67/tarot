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

import hashlib
from PyQt4 import QtCore, QtXml

class ChannelList(list):
    def get_by_name(self, name):
        for channel in self:
            if channel.name == name:
                return channel
        return None
    
    def to_xml(self):
        node = QtXml.QDomElement()
        node.setTagName("channel_list")
        for channel in self:
            node.appendChild(channel.to_xml())
        return node
    
    def from_xml(self, node):
        child = node.firstChildElement()   
        while not child.isNull():
            if child.tagName() == "channel":
                channel = Channel()
                channel.from_xml(child)
                self.append(channel)
            child = child.nextSiblingElement()

class Channel(QtCore.QObject):
    def __init__(self, name=None, email=None, password=None):
        QtCore.QObject.__init__(self)
        
        self.name = name
        self._password = password
    
    def __repr__(self):
        return "Channel(name=%s,_password=%s)" % (
            self.name,
            self._password
        )
    
    def to_xml(self):
        channel = QtXml.QDomElement()
        channel.setTagName("channel")
        channel.setAttribute("name", self.name)
        channel.setAttribute("password", self._password)
        return channel
        
    def from_xml(self, node):
        self.name =  node.attribute("name")
        self._password = node.attribute("password")
    
    def verify_password(self, password):
        hash = hashlib.sha512(password)
        if self._password == "%":
            return True
        if self._password == hash.hexdigest():
            return True
        return False
        
    def set_password(self, password):
        if password == "%":
            self._password = "%"
            return
        hash = hashlib.sha512(password)
        self._password = hash.hexdigest()
