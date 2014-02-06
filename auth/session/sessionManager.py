import sys
from .. import config
from . import dictAdapter
from . import flaskAdapter
from . import tornadoAdapter


ADAPTERS = {
    'dict': 'dictAdapter',
    'Flask': 'flaskAdapter',
    'tornado': 'tornadoAdapter'
}

current_module = thismodule = sys.modules[__name__]

class sManager(object):
    adapter = None

    @staticmethod
    def set_session(adapter = None):
        sess_adapter = adapter if adapter else config.G_SESSION
        sManager.adapter = getattr(current_module, ADAPTERS[sess_adapter]).Session

        return sManager.adapter

