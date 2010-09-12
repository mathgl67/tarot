
from xml.dom import minidom

from PyQt4.Qt import qDebug

from tarot.server.user import UserList
from tarot.server.chan import ChannelList

class ConfigStore(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.listen_host = None
        self.listen_port = None
        self.user_list = None
        self.channel_list = None
    
    def load(self):
        qDebug("read config file: %s" % self.file_path)
        with open(self.file_path, "r") as f:
            content = f.read()
            qDebug("parse config file")
            document = minidom.parseString(content)
            root = document.childNodes[0]
            self.from_xml(root)    
        
    def save(self):
        qDebug("save config file" % self.file_path)
        document = minidom.Document()
        document.appendChild(self.to_xml())
        
        with open(self.file_path, "w") as f:
            f.write(document.toprettyxml())
    
    def to_xml(self):
        config = minidom.Element("config")
        listen = minidom.Element("listen")
        listen.setAttribute("host", self.host)
        listen.setAttribute("port", str(self.port))
        config.appendChild(listen)
                
        if self.user_list:
            config.appendChild(self.user_list.to_xml())
            
        if self.channel_list:
            config.appendChild(self.channel_list.to_xml())
            
        return config
    
    def from_xml(self, node):
        if node.nodeName != "config":
            return False        
        
        for child in node.childNodes:
            if child.nodeName == "listen":
                self.host = child.getAttribute("host")
                self.port = int(child.getAttribute("port"))
            elif child.nodeName == "user_list":
                self.user_list = UserList()
                self.user_list.from_xml(child)
            elif child.nodeName == "channel_list":
                self.channel_list = ChannelList()
                self.channel_list.from_xml(child) 

        return True