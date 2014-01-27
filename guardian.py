import importlib
import hash

from authexception import AuthException
from config import *

### Importing UserModel from config
UserModel = importlib.import_module(G_MODEL).UserModel
### Importing Session from config
Session = importlib.import_module(G_SESSION).Session


""" Just in case i want to switch from Flask built in sessions to a db based session """

""" Or in case i want to switch from my sql Model, to a real ORM """

class Guardian(object):
    db = None
    def __init__(self, db = None):
        if db is not None:
            self.set_db(db)

        self.auth_user = None
        self.session = Session()

    def set_db(self, db):
        self.db = db
        self.UserModel = UserModel(db = self.db)

    def __user_exists(self, username):
        return self.UserModel.find_by_username(username)

    def authenticate(self, **kwargs):
        if self.db is None:
            raise AuthException('Could not connect to the database')

        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if username is None or username == '':
            raise AuthException('Username is missing')
    
        if password is None or password == '':
            raise AuthException('Password is missing')

        encPass = hashlib.sha512(password).hexdigest()

        user = self.__user_exists(username)

        if user is not None:
            if user.password == encPass:
                return True, [username, user.role]           

        raise AuthException('Username does not exist !') 

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


