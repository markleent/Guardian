import sqlite3

class UserModel:

    def __init__(self, **kwargs):
        self.db = kwargs.get('db', None)
        self.users = self.db.user
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
            last_id = self.users.insert({
                'username': self.username,
                'password': self.password,
                'role': self.role
            })
            self.set('id', last_id)
        else:
            self.users.update(
                {'username': self.username},
                {'$set': {
                    'username': self.username,
                    'password': self.password,
                    'role': self.role
                }}
            )

        return self

    def create(self, **kwargs):
        self.id = None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.role = kwargs.get('role', None)
        return self.save()


    def find(self, id):
        user = self.users.find_one({"_id": id})
        if user:
            self.__populate(user)
            return self

        return None 

    def find_by_username(self, username):
        user = self.users.find_one({
            'username': username
        })
        if user:
            self.__populate(user)
            return self

        return None


    def __populate(self, data):
        self.id = data['_id']
        self.username = data['username']
        self.password = data['password']
        self.role = data['role']