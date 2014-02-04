class Session(dict):
    def __init__(self, db = None):
        pass
        
    def set(self, item, value):
        setattr(self, item, value)

    def unset(self, item):
        setattr(self, item, None)

    def get(self, item):
        return self.item

    def haskey(self, item):
        return hasattr(self, item)