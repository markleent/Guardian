from flask import session

class Session:
    def __init__(self, db = None):
        pass

    def set(self, item, value):
        session[item] = value

    def unset(self, item):
        session.pop(item, None)

    def get(self, item):
        if self.haskey(item):
            return session[item]

        raise AttributeError('Attribute is not a valid Session key')

    def haskey(self, item):
        return item in session