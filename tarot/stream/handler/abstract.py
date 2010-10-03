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

class AbstractStreamHandler(QtCore.QObject):
    name=None
    
    def __init__(self, stream):
        QtCore.QObject.__init__(self)
        self.stream = stream
        
    def setup(self):
        self.input = self.stream.input
        self.output = self.stream.output
    
    def parse(self):
        self.attributes = self.input.parse_attributes()
    
    def run(self):
        pass

class StreamHandlerList(list):
    def __init__(self, stream):
        list.__init__(self)
        self.stream = stream
    
    def append(self, handler):
        if not isinstance(handler, AbstractStreamHandler):
            raise TypeError, "You can only append instance of AbstractHandlerStream class."
        list.append(self, handler)
        
    def from_class_list(self, class_list):
        if class_list:
            for cls in class_list:
                obj = cls(self.stream)
                self.append(obj)
        
    def get_by_name(self, name):
        for handler in self:
            if handler.name == name:
                return handler
        return None