from flask import session

class Session:
    def __init__(self, db = None):
        pass
        
    def set(self, item, value):
        session[item] = value

    def unset(self, item):
        session.pop(item, None)

    def get(self, item):
        return session[item]

    def haskey(self, item):
        return item in session