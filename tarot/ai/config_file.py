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

import os.path
from ConfigParser import ConfigParser

class AiConfigFile(ConfigParser):
    def __init__(self, config_path):
        super(AiConfigFile, self).__init__()
        self.config_path = config_path
        self.file_name = "ai.ini"
        self.file_full_path = os.path.join(self.config_path, self.file_name)
        self.path = None
        self.default = None

    def load(self):
        self.read(self.file_full_path)
        self.path = self.get("ai", "path")
        self.default = self.get("ai", "default")
        
    def save(self):
        self.set("ai", "path", self.path)
        self.set("ai", "default", self.default)
        self.write(file(self.file_full_path, "w+"))