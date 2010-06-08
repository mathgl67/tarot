'''
Created on 8 juin 2010

@author: mathgl
'''

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
        self.write(file(self.file_full_path, "w+")