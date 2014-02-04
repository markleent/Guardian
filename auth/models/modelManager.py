import sys
import auth.config
import auth.models.sql3Adapter as sql3Adapter
import auth.models.alchemyAdapter as alchemyAdapter
import auth.models.mongoAdapter as mongoAdapter

ADAPTERS = {
    'sqlite3': 'sql3Adapter',
    'sqlAlchemy': 'alchemyAdapter',
    'pymongo': 'mongoAdapter'
}

current_module = thismodule = sys.modules[__name__]

class mManager(object):

    def __init__(self):
        pass

    def set_model(self, adapter = None):
        model_adapter = adapter if adapter else auth.config.G_MODEL
        self.model = getattr(current_module, ADAPTERS[model_adapter]).UserModel

        return self.model

