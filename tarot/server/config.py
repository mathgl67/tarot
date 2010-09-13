

from PyQt4 import QtCore, QtXml
from PyQt4.Qt import qDebug, qCritical

from tarot.server.user import UserList
from tarot.server.chan import ChannelList

class ConfigStore(QtCore.QObject):
    def __init__(self, file_path):
        QtCore.QObject.__init__(self)
        
        self.file_path = file_path
        self.listen_host = None
        self.listen_port = None
        self.user_list = None
        self.channel_list = None
    
    def load(self):
        qDebug("config: read file: %s" % self.file_path)
        with open(self.file_path, "r") as f:
            content = f.read()
            qDebug("config: parse xml")
            document = QtXml.QDomDocument()
            document.setContent(content)
            (ret, error_msg, error_line, error_column) = document.setContent(content)
            if not ret:
                qDebug("file content: %s" % (content)) 
                qCritical("error: %s (line=%d;column=%d)" % (error_msg, error_line, error_column))
                return False
            
            qDebug("config: xml parsed")   
            
            return self.from_xml(document.firstChildElement())    
        
    def save(self):
        qDebug("save config file" % self.file_path)
        document = QtXml.QDomDocument()
        document.appendChild(self.to_xml())
        
        with open(self.file_path, "w") as f:
            f.write(document.toString())
    
    def to_xml(self):
        config = QtXml.QDomElement()
        config.setTagName("config")
        
        listen = QtXml.QDomElement()
        listen.setTagName("listen")
        listen.setAttribute("host", self.host)
        listen.setAttribute("port", str(self.port))
        
        config.appendChild(listen)
                
        if self.user_list:
            config.appendChild(self.user_list.to_xml())
            
        if self.channel_list:
            config.appendChild(self.channel_list.to_xml())
            
        return config
    
    def from_xml(self, node):
        qDebug("config: importing xml dom")
        if node.tagName() != "config":
            qCritical("config: first element is not the 'config' Element")
            return False        
        
        child = node.firstChildElement()
        while not child.isNull():
            qDebug("config: child name '%s'" % child.tagName())
            if child.tagName() == "listen":
                self.host = child.attribute("host")
                self.port = int(child.attribute("port"))
            elif child.tagName() == "user_list":
                self.user_list = UserList()
                self.user_list.from_xml(child)
            elif child.tagName() == "channel_list":
                self.channel_list = ChannelList()
                self.channel_list.from_xml(child)
            child = child.nextSiblingElement() 

        return True
    