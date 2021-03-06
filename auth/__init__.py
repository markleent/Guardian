# -*- coding: utf-8 -*-
from . import hasher as hash
from .authexception import AuthException
from . import config
from functools import wraps
from .models.modelManager import mManager
from .session.sessionManager import sManager
from .redirectors.redirectorManager import rManager

import simplevalidator

sessionMngr = sManager
modelMngr = mManager
redirMngr = rManager



__version__ = "0.0.4.3"

class Guardian(object):
    def __init__(self, app_context=None):
        self.db = None
        self.auth_user = None

        ### init settings if there is a database connection instance
        if config.G_DATABASE_POINTER:
            self.set_settings()

        if app_context:
            self.app = app_context

    def set_settings(self, db = None):
        self.db = db if db else config.G_DATABASE_POINTER
        self.set_model(config.G_MODEL)
        self.set_session(config.G_SESSION)

    def set_model(self, model = None):
        self.UserModel = modelMngr.set_model(model)(db = self.db)

    def set_session(self, session = None):
        self.session = sessionMngr.set_session(session)()

    ### This part is framework dependant, i will add a hook later
    def reload_user(self):
        try:
            if self.session.get('user_id'):
                self.login_user(self.__get_user_by_id(self.session.get('user_id')))
        except AttributeError:
            pass

    def unset_user(self):
        self.auth_user = None

    def __user_exists(self, username):
        return self.UserModel.find_by_username(username)

    def __get_user_by_id(self, id):
        return self.UserModel.find(id)

    def authenticate(self, **kwargs):
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)


        validate = simplevalidator.Validator(fields = kwargs, rules = {
            'username' : 'required', 
            'password': 'required',
        })

        if validate.fails():
            raise AuthException(validate.errors()[0])

        user = self.__user_exists(username)

        if user is not None:
            if hash.check(password, user.password):
                self.auth_user = user
                return True         

        raise AuthException('Username or password incorrect') 

    def create(self, **kwargs):
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        role = kwargs.get('role', 0)

        validate = simplevalidator.Validator(fields = kwargs, rules = {
            'username' : 'required', 
            'password': 'required',
        })

        if validate.fails():
            raise AuthException(validate.errors()[0])

        if role is None or (role != '1' and role != '0'):
            role = 0

        if self.__user_exists(username) is not None:
            raise AuthException('This username already exists')

        encPass = hash.make(password)

        return self.UserModel.create(username = username, password = encPass, role = role)

    def check(self):
        return self.session.haskey('user_id') and isinstance(self.auth_user, modelMngr.model)

    def user(self):
        return self.auth_user if isinstance(self.auth_user, modelMngr.model) else {}

    def login(self, username, password):
        if (self.authenticate(username = username, password = password)):
            self.session.set('user_id', self.auth_user.id)

        return True

    def login_user(self, user):
        
        if not isinstance(user, modelMngr.model):
            raise TypeError('user is not an instance of UserModel')

        self.auth_user = user
        self.session.set('user_id', user.id)

        return True

    def logout(self):
        self.auth_user = None
        self.session.unset('user_id')

    def require_login(self, f):
        
        def get_redirector():
            return redirMngr.set_redirector()

        @wraps(f)
        def is_authenticated(*args, **kwargs):
            if not self.check():
                return get_redirector()()
            return f(*args, **kwargs)

        return is_authenticated
