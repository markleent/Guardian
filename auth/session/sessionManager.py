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

    def __init__(self):
        pass

    def set_session(self, adapter = None):
        sess_adapter = adapter if adapter else config.G_SESSION
        self.adapter = getattr(current_module, ADAPTERS[sess_adapter]).Session

        return self.adapter

