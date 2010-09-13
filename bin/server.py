#!/usr/bin/env python

from tarot.server.config import ConfigStore
from tarot.server.socket import TcpServer

import sys
from PyQt4 import QtCore
from PyQt4.Qt import qDebug, qFatal


if __name__ == '__main__':
    qDebug("create the application object")
    app = QtCore.QCoreApplication(sys.argv)
    
    qDebug("load config file")
    config_store = ConfigStore("config/server.xml")
    if not config_store.load():
        qFatal("cannot load config file")
        sys.exit(1)

    qDebug("create tcp server and listen")
    server = TcpServer(app, config_store)
    if not server.listen():
        qFatal("cannot listen: %s" % server.errorString())
        sys.exit(2)    

    sys.exit(app.exec_())
