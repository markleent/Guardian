import sys
import auth.config
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

try:
    import auth.session.dictAdapter as dictAdapter
except ImportError:
    if auth.config.DEBUG:
        logging.warning('Import Error: %s', 'Null Session (dictAdapter) could not be imported, please check if you need this')

try:
    import auth.session.flaskAdapter as flaskAdapter
except ImportError:
    if config.DEBUG:
        logging.warning('Import Error: %s', 'flask Session (flaskAdapter) could not be imported, please check if you need this')

try:
    import auth.session.tornadoAdapter as tornadoAdapter
except ImportError:
    if auth.auth.config.DEBUG:
        logging.warning('Import Error: %s', 'tornado Session (tornadoAdapter) could not be imported, please check if you need this')


ADAPTERS = {
    'dict': 'dictAdapter',
    'Flask': 'flaskAdapter',
    'tornado': 'tornadoAdapter'
}

current_module = thismodule = sys.modules[__name__]

class sManager(object):

    def __init__(self, adapter = None):

        if adapter:
            self.set_model(adapter)

    def set_session(self, adapter = None):
        sess_adapter = adapter if adapter else auth.config.G_SESSION
        self.adapter = getattr(current_module, ADAPTERS[sess_adapter]).Session

        return self.adapter

