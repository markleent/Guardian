# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import bcrypt
import uuid

""" 
    force hash module to always output utf8 strings instead of bytes
    as it's going to be stored in a database for later use
"""
def make(word):
    enc_word = word
    prep_salt = uuid.uuid4().hex
    salt = ("$2a$06$" + hashlib.sha512(prep_salt).hexdigest()[0:22] + "$").encode('utf-8')

    output = bcrypt.hashpw(enc_word, salt)
    
    return output

def check(word, hash):
    return bcrypt.hashpw(word, hash.encode('utf-8')) == hash