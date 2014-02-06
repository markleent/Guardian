### NullRedirector, dummy file for dict base redirectors :)
from .. import config

def Redirect():
    return 'You have been redirected to ' + config.REDIRECT_URI