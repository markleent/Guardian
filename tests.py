# -*- coding: utf-8 -*-

from db_con import connect_db
from pymongo import MongoClient
from sqlalchemy import create_engine
import auth
import unittest
import sys


engine = create_engine('sqlite:///test.db', echo=True)

class AuthTestsSQL3(unittest.TestCase):
    
    def setUp(self):
        auth.config.G_DATABASE_POINTER = connect_db('test.db')

        from auth.models.sql3Adapter import UserModel
        setattr(auth, 'UserModel', UserModel)

        self.Guard = auth.Guardian()

    def test_authenticate_pass(self):

        self.assertTrue(self.Guard.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            self.Guard.authenticate(username = "admin", password = "password2")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


    def test_creaste_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')

    def test_empty_auth(self):

        self.assertFalse(self.Guard.user())

    def test_auth_user(self):

        self.Guard.authenticate(username = "admin", password = "password")
        self.assertTrue(self.Guard.user().username == 'admin')

class AuthTestsMONGO(unittest.TestCase):
    
    def setUp(self):
        _client = MongoClient('localhost')
        database = _client['Guardian_test_db']

        ### Hacky solution but this is for the test only, while it might not be beautiful pythonic code
        ### atleast it actually works ;) that it actually works/switch on the fly !
        from auth.models.mongoAdapter import UserModel
        setattr(auth, 'UserModel', UserModel)

        ### clean up of the database for each run
        database.user.drop()

        auth.config.G_DATABASE_POINTER = database
        self.Guard = auth.Guardian()

        self.Guard.create(username = 'admin', password = 'password')

    def test_authenticate_pass(self):

        self.assertTrue(self.Guard.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            self.Guard.authenticate(username = "admin", password = "password2")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


    def test_creaste_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')

    def test_empty_auth(self):

        self.assertFalse(self.Guard.user())

    def test_auth_user(self):

        self.Guard.authenticate(username = "admin", password = "password")
        self.assertTrue(self.Guard.user().username == 'admin')

class AuthTestsSQLalchemy(unittest.TestCase):
    
    def setUp(self):
        ### Hacky solution but this is for the test only, while it might not be beautiful pythonic code
        ### atleast it actually works ;) that it actually works/switch on the fly !
        from auth.models.alchemyAdapter import UserModel
        setattr(auth, 'UserModel', UserModel)

        auth.config.G_DATABASE_POINTER = engine
        self.Guard = auth.Guardian()

    def test_authenticate_pass(self):

        self.assertTrue(self.Guard.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            self.Guard.authenticate(username = "admin", password = "password2")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


    def test_creaste_validation_fail(self):

        try:
            self.Guard.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')

    def test_empty_auth(self):

        self.assertFalse(self.Guard.user())

    def test_auth_user(self):

        self.Guard.authenticate(username = "admin", password = "password")
        self.assertTrue(self.Guard.user().username == 'admin')


if __name__ == '__main__':
    unittest.main()