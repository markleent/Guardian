from .. import config
import simplevalidator
from flask import redirect, url_for

def Redirect():
    v = simplevalidator.Validator()
    v.make(fields = {'uri': config.REDIRECT_URI}, rules = {'uri' : 'url'})

    if v.fails():
        return redirect(url_for(config.REDIRECT_URI))

    return redirect(config.REDIRECT_URI)
