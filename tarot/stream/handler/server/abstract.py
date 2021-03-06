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

from tarot.stream.handler.abstract import AbstractStreamHandler

class AbstractServerStreamHandler(AbstractStreamHandler):
    must_be_auth=True
    must_be_admin=False
    
    def setup(self):
        AbstractStreamHandler.setup(self)
        self.output_channel = self.stream.output_channel
        self.session = self.stream.context
        self.server = self.stream.context.server
    
    def allowed(self):
        if self.must_be_auth and not self.session.user:
            return False
        
        if self.must_be_admin and self.session.user and not self.session.user.is_admin:
            return False
        
        return True
    