
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
    def channel_users(session_list):
        (doc, root) = Message.prepare_document("channel-users")
        for session in session_list:
            user = doc.createElement("user")
            user.setAttribute("name", session.user.name)
            root.appendChild(user)
        return Message.to_string(doc)
