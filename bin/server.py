#!/usr/bin/env python

from tarot.server.config import ConfigStore
from tarot.server.socket import TcpServer

import sys
from PyQt4 import QtCore


if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    
    config_store = ConfigStore("test.xml")
    config_store.load()

    server = TcpServer(app, config_store)
    if not server.listen():
        print "Cannot listen:", server.errorString()
        sys.exit(-1)    

    sys.exit(app.exec_())
