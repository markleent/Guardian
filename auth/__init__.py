# -*- coding: utf-8 -*-
import importlib
import auth.hash
from auth.authexception import AuthException
from auth.config import *

### Importing UserModel from config
UserModel = importlib.import_module(G_MODEL).UserModel
### Importing Session from config
Session = importlib.import_module(G_SESSION).Session

from ..validation.simplevalidator import Validator

class Guardian(object):
    def __init__(self):
        self.db = None
        self.auth_user = None
        self.set_settings()

    def set_settings(self, db = None):
        self.db = db if db else G_DATABASE
        self.UserModel = UserModel(db = self.db)
        self.session = Session()

    def __user_exists(self, username):
        return self.UserModel.find_by_username(username)

    def authenticate(self, **kwargs):
        if self.db is None:
            raise AuthException('Could not connect to the database')

        username = kwargs.get('username', None)
        password = kwargs.get('password', None)


        validate = Validator(fields = kwargs, rules = {
            'username' : 'required', 
            'password': 'required',
        })

        if validate.fails():
            raise AuthException(validate.errors()[0])

        user = self.__user_exists(username)

        if user is not None:
            if hash.check(password, user.password):
                self.auth_user = user
                return True, [user.username, user.role]           

        raise AuthException('Username or password incorrect') 

    def create(self, **kwargs):
        if self.db is None:
            raise AuthException('Could not connect to the database')

        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        role = kwargs.get('role', 0)

        if username is None or username == '':
            raise AuthException('Username is missing')
    
        if password is None or password == '':
            raise AuthException('Password is missing')

        if role is None or (role != '1' and role != '0'):
            role = 0

        if self.__user_exists(username) is not None:
            raise AuthException('This username already exists')

        encPass = hashlib.sha512(password).hexdigest()

        return self.UserModel.create(username = username, password = encPass, role = role)

    def check(self):
        return self.user is not None

    def user(self):
        return self.auth_user if self.auth_user else {}

    """ Wrapper methods because i am making a lib like i am going to reuse it :D """    
    def register(self, username, password, role):
        self.create(username = username, password = password, role = role)

    def login(self, user):
        
        if not isinstance(user, UserModel):
            raise TypeError('user is not an instance of UserModel')

        self.auth_user = user
        #userData  = self.authenticate(username = username, password = password)[1]
        #self.session.set('username', userData[0])
        #self.session.set('role', userData[1])

    def logout(self):
        self.auth_user = None
        #self.session.unset('username')
        #self.session.unset('role')

    def check(self):
        return self.session.haskey('username')