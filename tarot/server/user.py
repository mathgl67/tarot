
import hashlib
from xml.dom import minidom

class UserList(list):
    def get_by_name(self, name):
        for user in self:
            if user.name == name:
                return user
        return None
    
    def to_xml(self):
        node = minidom.Element("user_list")
        for user in self:
            node.appendChild(user.to_xml())
        return node
    
    def from_xml(self, node):           
        for child in node.childNodes:
            if child.nodeName == "user":
                user = User()
                user.from_xml(child)
                self.append(user)

class User(object):
    def __init__(self, name=None, email=None, groups=None, password=None):
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
        user = minidom.Element("user")
        user.setAttribute("name", self.name)
        user.setAttribute("email", self.email)
        user.setAttribute("is_admin", "yes" if self.is_admin else "no")
        user.setAttribute("password", self._password)
        
        return user
        
    def from_xml(self, node):
        self.name =  node.getAttribute("name")
        self.email = node.getAttribute("email")
        self.is_admin = True if node.getAttribute("is_admin") == "yes" else False
        self._password = node.getAttribute("password")
    
    def verify_password(self, password):
        hash = hashlib.sha512(password)
        print "hash:", hash.hexdigest()
        if self._password == hash.hexdigest():
            return True
        return False
        
    def set_password(self, password):
        hash = hashlib.sha512(password)
        self._password = hash.hexdigest()
