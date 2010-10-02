#!/usr/bin/env python
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

from tarot.server.config import ConfigStore
from tarot.server.server import Server

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
    server = Server(app, config_store)
    if not server.listen():
        qFatal("cannot listen: %s" % server.errorString())
        sys.exit(2)    

    sys.exit(app.exec_())
