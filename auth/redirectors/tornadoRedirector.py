### NullRedirector, dummy file for yet to come Tornado redirector
from .. import config

def Redirect():
    return 'You have been redirected to ' + config.REDIRECT_URI