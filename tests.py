# -*- coding: utf-8 -*-

from db_con import connect_db
from pymongo import MongoClient
from sqlalchemy import create_engine
import auth
import unittest
import sys

Auth = auth.Guardian()


class AuthTestsDefaults:

    def test_authenticate_pass(self):

        self.assertTrue(Auth.authenticate(username = "admin", password = "password"))

    def test_authenticate_fail(self):

        try:
            Auth.authenticate(username = "admin", password = "password2")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'Username or password incorrect')

    def test_authenticate_validation_fail(self):

        try:
            Auth.authenticate(username = "", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')


    def test_authenticate_validation_fail(self):

        try:
            Auth.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')


    def test_creaste_validation_fail(self):

        try:
            Auth.authenticate(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')

    def test_empty_auth(self):

        self.assertFalse(Auth.user())

    def test_auth_user(self):

        Auth.authenticate(username = "admin", password = "password")
        self.assertTrue(Auth.user().username == 'admin')

    def test_check_decorator_not_logged_in(self):

        @Auth.require_login
        def test_this():
            return "i am logged in"

        self.assertTrue("You are being redirected !!" == test_this())


    def test_check_decorator_logged_in(self):

        Auth.login('admin', 'password')

        @Auth.require_login
        def test_this():
            return "i am logged in"

        self.assertTrue("i am logged in" == test_this())

    def test_create_user_username_fail(self):

        try:
            Auth.create(username = "", password = "password")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'username is required')

    def test_create_user_username_fail(self):

        try:
            Auth.create(username = "test_user", password = "")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'password is required')

    def test_create_log_delete_user_pass(self):

        self.assertTrue(Auth.create(username = "test_user", password = "password"))

        self.assertTrue(Auth.login(username = "test_user", password = "password"))

        self.assertTrue(Auth.user().delete())

    def teste_create_user_already_exists(self):

        try:
            Auth.create(username = "admin", password = "mynewpassword !!!")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'This username already exists')



class AuthTestsSQL3(unittest.TestCase, AuthTestsDefaults):

    @classmethod
    def setUpClass(cls):
        auth.config.G_DATABASE_POINTER = connect_db('test.db')
        auth.config.G_MODEL = 'sqlite3'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.close()

    def setUp(self):
        Auth.logout()



class AuthTestsMONGO(unittest.TestCase, AuthTestsDefaults):

    @classmethod
    def setUpClass(cls):
        cls._client = MongoClient('localhost')

        auth.config.G_DATABASE_POINTER = cls._client['Guardian_test_db']
        auth.config.G_MODEL = 'pymongo'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

    @classmethod
    def tearDownClass(cls):
        cls._client.close()
    
    def setUp(self):
        Auth.logout()
        auth.config.G_DATABASE_POINTER.user.drop()
        Auth.create(username = 'admin', password = 'password')


class AuthTestsSQLalchemy(unittest.TestCase, AuthTestsDefaults):
    
    @classmethod
    def setUpClass(cls):

        auth.config.G_DATABASE_POINTER = create_engine('sqlite:///test.db', echo=False)
        auth.config.G_MODEL = 'sqlAlchemy'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.dispose()
    
    def setUp(self):
        Auth.logout()



if __name__ == '__main__':
    unittest.main()