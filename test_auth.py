# -*- coding: utf-8 -*-
#from __future__ import absolute_import

import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from db_con import connect_db
import auth
import unittest

guardian.G_DATABASE = connect_db('test.db')


Guard = auth.guardian.Guardian()

class AuthTests(unittest.TestCase):

    def test_authenticate_pass(self):

        self.assertTrue(Guard.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            Guard.authenticate(username = "admin", password = "password2")
        except auth.guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            Guard.authenticate(username = "", password = "")
        except auth.guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            Guard.authenticate(username = "", password = "password")
        except auth.guardian.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


if __name__ == '__main__':
    unittest.main()