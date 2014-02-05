import sys
import auth.config
import auth.session.dictAdapter as dictAdapter
import auth.session.flaskAdapter as flaskAdapter
import auth.session.tornadoAdapter as tornadoAdapter


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
        sess_adapter = adapter if adapter else auth.config.G_SESSION
        self.adapter = getattr(current_module, ADAPTERS[sess_adapter]).Session

        return self.adapter

