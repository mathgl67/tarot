
import hashlib
from xml.dom import minidom

class ChannelList(list):
    def get_by_name(self, name):
        for channel in self:
            if channel.name == name:
                return channel
        return None
    
    def to_xml(self):
        node = minidom.Element("channel_list")
        for channel in self:
            node.appendChild(channel.to_xml())
        return node
    
    def from_xml(self, node):           
        for child in node.childNodes:
            if child.nodeName == "channel":
                channel = Channel()
                channel.from_xml(child)
                self.append(channel)

class Channel(object):
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self._password = password
    
    def __repr__(self):
        return "Channel(name=%s,_password=%s)" % (
            self.name,
            self._password
        )
    
    def to_xml(self):
        channel = minidom.Element("channel")
        channel.setAttribute("name", self.name)
        channel.setAttribute("password", self._password)
        return channel
        
    def from_xml(self, node):
        self.name =  node.getAttribute("name")
        self._password = node.getAttribute("password")
    
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
