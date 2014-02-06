import sys
from .. import config
from . import sql3Adapter
from . import alchemyAdapter
from . import mongoAdapter

ADAPTERS = {
    'sqlite3': 'sql3Adapter',
    'sqlAlchemy': 'alchemyAdapter',
    'pymongo': 'mongoAdapter'
}

current_module = thismodule = sys.modules[__name__]

class mManager(object):
    model = None

    @staticmethod
    def set_model(adapter = None):
        model_adapter = adapter if adapter else config.G_MODEL
        mManager.model = getattr(current_module, ADAPTERS[model_adapter]).UserModel

        return mManager.model

