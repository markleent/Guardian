from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Session = sessionmaker()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(Integer)


class UserModel:

    def __init__(self, **kwargs):
        
        ### SqlAlchemy specific thingies
        Session.configure(bind=kwargs.get('db', None))
        self.session = Session()
        
        self.id = None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.role = kwargs.get('role', None)

    def set(self, item, value):
        self.item = value

    def get(self, item):
        return self.item

    def save(self):
        
        if self.id is None:
            new_user = User(username = self.username, password = self.password, role = self.role)
            self.session.add(new_user).commit()
            self.set('id', new_user.id)
        else:

            ### we keep the state of the user inside the class instance, and refresh data on the fly through sqlAlchemy
            user = self.session.query(User).filter_by(id=self.id).first()
            user.username = self.username
            user.password = self.password
            user.role = self.role
            self.session.add(user).commit()

        return self

    def create(self, **kwargs):
        self.id = None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.role = kwargs.get('role', None)
        return self.save()


    def find(self, id):
        user = self.session.query(User).filter_by(id=id).first()
        if user:
            self.__populate(user)
            return self

        return None 

    def find_by_username(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            self.__populate(user)
            return self

        return None

    def __reset(self):
        self.id = None
        self.username = None
        self.password = None
        self.role = None
        
    def __populate(self, data):
        self.id = data.id
        self.username = data.username
        self.password = data.password
        self.role = data.role