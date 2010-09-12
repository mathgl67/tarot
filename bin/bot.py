#!/usr/bin/env python

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
