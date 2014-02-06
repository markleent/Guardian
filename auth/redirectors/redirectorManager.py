import sys
from .. import config
from . import nullRedirector
from . import flaskRedirector
from . import tornadoRedirector


ADAPTERS = {
    'dict': 'nullRedirector',
    'Flask': 'flaskRedirector',
    'tornado': 'tornadoRedirector'
}

current_module = thismodule = sys.modules[__name__]

class rManager(object):

    @staticmethod
    def set_redirector(adapter = None):
        sess_adapter = adapter if adapter else config.G_SESSION

        return getattr(current_module, ADAPTERS[sess_adapter]).Redirect

