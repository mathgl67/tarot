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

class UserList(list):
    def get_by_name(self, name):
        for user in self:
            if user.name == name:
                return user
        return None
    
    def to_xml(self):
        node = QtXml.QDomElement()
        node.setTagName("user_list")
        for user in self:
            node.appendChild(user.to_xml())
        return node
    
    def from_xml(self, node):
        child = node.firstChildElement()    
        while not child.isNull():
            if child.tagName() == "user":
                user = User()
                user.from_xml(child)
                self.append(user)
            child = child.nextSiblingElement()

class User(QtCore.QObject):
    def __init__(self, name=None, email=None, groups=None, password=None):
        QtCore.QObject.__init__(self)
        
        self.name = name
        self.email = email
        self.is_admin = False
        self._password = password
    
    def __repr__(self):
        return "User(name=%s,email=%s,is_admin=%s)" % (
            self.name,
            self.email,
            self.is_admin,
        )
    
    def to_xml(self):
        user = QtXml.QDomElement()
        user.setTagName("user")
        user.setAttribute("name", self.name)
        user.setAttribute("email", self.email)
        user.setAttribute("is_admin", "yes" if self.is_admin else "no")
        user.setAttribute("password", self._password)
        return user
        
    def from_xml(self, node):
        self.name =  node.attribute("name")
        self.email = node.attribute("email")
        self.is_admin = True if node.attribute("is_admin") == "yes" else False
        self._password = node.attribute("password")
    
    def verify_password(self, password):
        hash = hashlib.sha512(password)
        print "hash:", hash.hexdigest()
        if self._password == hash.hexdigest():
            return True
        return False
        
    def set_password(self, password):
        hash = hashlib.sha512(password)
        self._password = hash.hexdigest()
