# -*- coding: utf-8 -*-

import hashlib
import bcrypt
import uuid

""" 
    force hash module to always output utf8 strings instead of bytes
    as it's going to be stored in a database for later use
"""
def make(word):
    enc_word = word.encode('utf-8')
    prep_salt = uuid.uuid4().hex.encode('utf-8')
    salt = ("$2a$06$" + hashlib.sha512(prep_salt).hexdigest()[0:22] + "$").encode('utf-8')

    output = bcrypt.hashpw(enc_word, salt)

    if isinstance(output, str):
        return output
    else:
        return output.decode(encoding='utf-8')

def check(word, hash):
    return bcrypt.hashpw(word.encode('utf-8'), hash.encode('utf-8')).decode('utf-8') == hash