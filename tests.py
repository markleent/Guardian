# -*- coding: utf-8 -*-

from db_con import connect_db
from pymongo import MongoClient
from sqlalchemy import create_engine
import auth
import unittest
import sys
import flaskapp
from mock import Mock

from auth.models.modelManager import mManager

Auth = auth.Guardian()

### Models Tests
class AuthModelsDefaults:

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

    ### Note the following method are just to test that the decorator is fired
    ### It is not the final test !
    def test_check_decorator_not_logged_in(self):

        @Auth.require_login
        def test_this():
            return "i am logged in"

        self.assertTrue("You are being redirected !!" == test_this())

    ### Note the following method are just to test that the decorator is fired
    ### It is not the final test !
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

        self.assertTrue(Auth.login("test_user", "password"))

        self.assertTrue(Auth.user().delete())

    def test_create_user_already_exists(self):

        try:
            Auth.create(username = "admin", password = "mynewpassword !!!")
        except auth.AuthException as e:
            self.assertRaisesRegexp(e, 'This username already exists')

    def test_user_set_get(self):

        Auth.login('admin', 'password')

        Auth.user().set('car', 32)

        self.assertTrue(Auth.user().get('car') == 32)


    def test_manager_find_by_id_pass(self):

        ### Ids are automatic, so we have to use a small trick, here ;)
        user = self.mManager.find_by_username('admin')

        user_id = user.id

        user = None

        user = self.mManager.find(user_id)

        self.assertTrue(user.username == 'admin')


    def test_manager_find_by_id_fail(self):

        user = self.mManager.find(-2)

        self.assertFalse(user)

    ### modify role
    def test_manager_save_role(self):

        user = self.mManager.find_by_username('admin')

        ### change user role from admin to simple user
        user.role = 0

        self.assertTrue(user.save())

    ### verify role in subsequent call
    def test_manager_save_state(self):

        user = self.mManager.find_by_username('admin')

        self.assertTrue(user.role == 0)

    ### reverse role
    def test_manager_save_state_reverse(self):

        Auth.login('admin', 'password')

        Auth.user().role = 1

        self.assertTrue(Auth.user().save())

    ### Load a user through the manager, and then log him back !
    def test_manager_log_user_programatically_pass(self):

        ### We make sure that no user is currently Authenticated
        self.assertFalse(Auth.user())

        ### Load user
        user = self.mManager.find_by_username('admin')

        Auth.login_user(user)

        ### check that we are indeed logged as admin
        self.assertTrue(Auth.check())
        self.assertTrue(Auth.user().username == "admin")

    def test_manager_log_user_programatically_pass(self):

        ### We make sure that no user is currently Authenticated
        self.assertFalse(Auth.user())

        ### Load user
        user = "I am a fake user, lol ?"

        ### we can't be logged in baby ! - note i am writing this test at.... 3am or so, pardon my French :P
        try:
            Auth.login_user(user)
        except TypeError as e:
            self.assertRaisesRegexp(e, 'user is not an instance of UserModel')

    def test_some_dictSession_that_coverall_doesnt_seem_to_cover(self):

        try:
            Auth.session.get('whoopsydoo')
        except AttributeError as e:
            self.assertRaisesRegexp(e, 'Attribute is not a valid Session key')



class AuthTestsSQL3(unittest.TestCase, AuthModelsDefaults):

    @classmethod
    def setUpClass(cls):
        auth.config.G_DATABASE_POINTER = connect_db('test.db')
        auth.config.G_MODEL = 'sqlite3'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

        ### manual call on the manager, it looks... dangerous ... :)
        cls.mManager = mManager().set_model('sqlite3')(db = auth.config.G_DATABASE_POINTER)

    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.close()

    def setUp(self):
        Auth.logout()



class AuthTestsMONGO(unittest.TestCase, AuthModelsDefaults):

    @classmethod
    def setUpClass(cls):
        cls._client = MongoClient('localhost')

        auth.config.G_DATABASE_POINTER = cls._client['Guardian_test_db']
        auth.config.G_MODEL = 'pymongo'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

        ### manual call on the manager, it looks... dangerous ... :)
        cls.mManager = mManager().set_model('pymongo')(db = auth.config.G_DATABASE_POINTER)

    @classmethod
    def tearDownClass(cls):
        cls._client.close()
    
    def setUp(self):
        Auth.logout()
        auth.config.G_DATABASE_POINTER.user.drop()
        Auth.create(username = 'admin', password = 'password')


class AuthTestsSQLalchemy(unittest.TestCase, AuthModelsDefaults):
    
    @classmethod
    def setUpClass(cls):

        auth.config.G_DATABASE_POINTER = create_engine('sqlite:///test.db', echo=False)
        auth.config.G_MODEL = 'sqlAlchemy'
        auth.config.G_SESSION = 'dict'

        Auth.set_settings()

        ### manual call on the manager, it looks... dangerous ... :)
        cls.mManager = mManager().set_model('sqlAlchemy')(db = auth.config.G_DATABASE_POINTER)

    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.dispose()
    
    def setUp(self):
        Auth.logout()

### Session Tests, in these tests we don't need to test each model implementations (as they are decoupled anyway)
### So we will use the default sqlite3 for the time being

### the dict/null session adapter doesn't need any context (as it is purely stateless)
### But to be able to test the suite without having to duplicate code, it is needed
mock_context = Mock()
mock_context.__enter__ = Mock(return_value='I am in')
mock_context.__exit__ = Mock(return_value=True)

class AuthSessionDefaults:

    def test_session_empty(self):
        with self.app:
            try:
                Auth.session.get('user_id_2342')
            except AttributeError as e:
                self.assertRaisesRegexp(e, 'Attribute is not a valid Session key')

    def test_session_pass(self):
        with self.app:
            Auth.login('admin', 'password')
            self.assertTrue(Auth.session.get('user_id'))

    def test_session_set(self):
        with self.app:
            Auth.login('admin', 'password')
            Auth.session.set('test', True)
            self.assertTrue(Auth.session.get('test'))


class AuthTestsSQL3_DICT(unittest.TestCase, AuthSessionDefaults):

    @classmethod
    def setUpClass(cls):
        auth.config.G_DATABASE_POINTER = connect_db('test.db')
        auth.config.G_MODEL = 'sqlite3'
        auth.config.G_SESSION = 'dict'
        Auth.set_settings()


    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.close()
        Auth.logout()

    def setUp(self):
        self.app = mock_context
        Auth.logout()



class AuthTestsSQL3_FLASK(unittest.TestCase, AuthSessionDefaults):

    @classmethod
    def setUpClass(cls):
        auth.config.G_DATABASE_POINTER = connect_db('test.db')
        auth.config.G_MODEL = 'sqlite3'
        auth.config.G_SESSION = 'Flask'
        Auth.set_settings()
        cls.app = flaskapp.app.test_request_context('/test')

    @classmethod
    def tearDownClass(cls):
        auth.config.G_DATABASE_POINTER.close()
        with cls.app:
            Auth.logout()

    def setUp(self):
        with self.app:
            Auth.logout()




"""
###Not yet implemented !
class AuthTestsSQL3_TORNADO(unittest.TestCase, AuthSessionDefaults):

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
"""

if __name__ == '__main__':
    unittest.main()