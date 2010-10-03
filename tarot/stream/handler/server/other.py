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

from tarot.stream.handler.server.abstract import AbstractServerStreamHandler

class ErrorStreamHandler(AbstractServerStreamHandler):
    name="error"
    must_be_auth=False
    
    def run(self):
        """
            <admin-shutdown />

        """
        print "error %s: %s" % (
            self.attributes["name"],
            self.attributes["message"] if self.attributes["message"] else "No error message."
        )

class AuthStreamHandler(AbstractServerStreamHandler):
    name="auth"
    must_be_auth=False
    
    def run(self):
        """
            <auth user="name" password="password" />
            
            return:
                * <auth result="success" />
                * <auth result="error" code="1" message="An error message" />
            
            code/message:
                1 - User or password incorrect
                2 - User already have a session
        """
        user_name = self.attributes.get("user", None)
        user = self.session.server.config_store.user_list.get_by_name(user_name)
        if user:
            print "user found"
            if user.verify_password(self.attributes.get("password", None)):
                print "user password okay"
                if not self.server.session_list.user_exists(user):
                    print "user %s authentified" % (user.name)
                    self.session.user = user
                    self.output.base("auth", { "result": "success" })
                    return
                else:
                    print "user %s already have a session" % (user.name)
                    self.output.base("auth", {
                        "result": "error",
                        "code": "2",
                        "message": "User already have a session."
                    })
                    return
        
        print "bad authententification"
        self.output.base("auth", {
            "result": "error",
            "code": "1",
            "message": "User or password incorrect"
        })

_module_handler_list = [ErrorStreamHandler, AuthStreamHandler]