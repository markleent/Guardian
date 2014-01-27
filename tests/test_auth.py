# -*- coding: utf-8 -*-

import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

#from mypackage.mymodule import as_int
from db_con import connect_db
import guardian
import unittest

guardian.G_DATABASE = connect_db('test.db')


Auth = guardian.Guardian()

class AuthTests(unittest.TestCase):

    def test_authenticate_pass(self):

        self.assertTrue(Auth.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            Auth.authenticate(username = "admin", password = "password2")
        except guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            Auth.authenticate(username = "", password = "")
        except guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            Auth.authenticate(username = "", password = "password")
        except guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


if __name__ == '__main__':
    unittest.main()