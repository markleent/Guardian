from flask import (Flask, json, request, g, redirect, url_for, abort, render_template, flash, Response)
import auth.config

app = Flask(__name__)
### This should be the other way around, but for testing purpose we take the config from the auth ;)
app.secret_key = auth.config.SESSION_SECRET

@app.route('/test')
def test():
    return 'Hello (test) World !'

@app.route('/login')
def login():
    return 'You have been redirected to login'

if __name__ == "__main__":
    app.run()