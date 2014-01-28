# -*- coding: utf-8 -*-
#from __future__ import absolute_import

from db_con import connect_db
import auth
import unittest

auth.G_DATABASE = connect_db('test.db')


Guard = auth.Guardian()

class AuthTests(unittest.TestCase):

    def test_authenticate_pass(self):

        self.assertTrue(Guard.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            Guard.authenticate(username = "admin", password = "password2")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            Guard.authenticate(username = "", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


if __name__ == '__main__':
    unittest.main()