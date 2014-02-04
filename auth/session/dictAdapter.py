class Session(dict):
    def __init__(self, db = None):
        pass
        
    def set(self, item, value):
        setattr(self, item, value)

    def unset(self, item):
        setattr(self, item, None)

    def get(self, item):
        if self.haskey(item):
            return getattr(self, item)

        raise AttributeError('Attribute is not a valid Session key')

    def haskey(self, item):
        return hasattr(self, item)