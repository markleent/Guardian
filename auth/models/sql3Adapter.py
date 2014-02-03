import sqlite3

class UserModel:

    def __init__(self, **kwargs):
        self.db = kwargs.get('db', None)
        self.db.row_factory = sqlite3.Row
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
            self.db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?);', [self.username, self.password, self.role])
            self.set('id', self.db.cursor().lastrowid)
        else:
            self.db.execute('UPDATE users set username = ?, password = ?, role = ? where id = ?', [self.username, self.password, self.role, self.id])

        self.db.commit()

        return self

    def create(self, **kwargs):
        self.id = None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.role = kwargs.get('role', None)
        return self.save()


    def find(self, id):
        user = self.db.execute('SELECT * from users WHERE id = ?;', [id]).fetchone()
        if user:
            self.__populate(user)
            return self

        return None 

    def find_by_username(self, username):
        user = self.db.execute('SELECT * from users WHERE username = ?;', [username]).fetchone()
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
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.role = data['role']