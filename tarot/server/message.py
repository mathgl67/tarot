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

from PyQt4 import QtXml

class Message(object):
    @staticmethod
    def prepare_document(root_element_name):
        doc = QtXml.QDomDocument()
        root = doc.createElement(root_element_name)
        doc.appendChild(root)
        return (doc, root)
    
    @staticmethod
    def to_string(document):
        string = document.toString()
        string.replace("\n", "") # This is bad...
        return string
    
    @staticmethod
    def simple(root_element_name, attributes=None):
        (doc, root) = Message.prepare_document(root_element_name)
        if attributes:
            for name, value in attributes.items():
                root.setAttribute(name, value)
        return Message.to_string(doc)
    
    @staticmethod
    def game_start(user_list):
        (doc, root) = Message.prepare_document("game-start")
        for user_name in user_list:
            user = doc.createElement("user")
            user.setAttribute("name", user_name)
            root.appendChild(user)
        return Message.to_string(doc)
        
    @staticmethod
    def channel_users(session_list):
        (doc, root) = Message.prepare_document("channel-users")
        for session in session_list:
            user = doc.createElement("user")
            user.setAttribute("name", session.user.name)
            root.appendChild(user)
        return Message.to_string(doc)
