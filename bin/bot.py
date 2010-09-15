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

import sys

from PyQt4 import QtCore
from tarot.bot import Bot

if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    
    bot1 = Bot({"user": "bot1", "user_password": "test", "channel": "chan1", "channel_password":"test"})
    bot1.connectToHost("127.0.0.1", 34888)
    bot1.quitRequested.connect(app.quit)
    
    bot2 = Bot({"user": "bot2", "user_password": "test", "channel": "chan1", "channel_password":"test"})
    bot2.connectToHost("127.0.0.1", 34888)
    bot2.quitRequested.connect(app.quit)
    
    bot3 = Bot({"user": "bot3", "user_password": "test", "channel": "chan1", "channel_password":"test"})
    bot3.connectToHost("127.0.0.1", 34888)
    bot3.quitRequested.connect(app.quit)
    
    sys.exit(app.exec_())
