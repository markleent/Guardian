Guardian
========

[![Build Status](https://travis-ci.org/markleent/Guardian.png?branch=master)](https://travis-ci.org/markleent/Guardian) [![Coverage Status](https://coveralls.io/repos/markleent/Guardian/badge.png?branch=master)](https://coveralls.io/r/markleent/Guardian?branch=master)

A work in progress, framework independant (with, hopefully some provided adapters !), simple Web Auth System in Python !

Here is the list of things i intend to integrate:
- DB based auth system (login, logout, create user, check etc)
- Support for sqlite3, mongodb, sqlAlchemy ORM through Adapters

Here is the list of things that i may integrate:
- Basic http auth
- Sessions (although this needs adapters to frameworks)

Here is the list of things i hope to integrate:
- Role based/perm based ACL


How to use it ?
===============

This library is to be init at your apps init, with the correct adapter for the user model, and inject the auth object inside your request handler, and use it as needed !

Or, in the case of a non web specific application, just asis !



Requirements
============

Dependecies:
    - bcrypt
    - simpleValidator
    - at least sqlite3 (or more databases through sqlAlchemy, if needed !)

Optional:
    - Flask, to handle session/basic http auth through Flask
    - Tornado, same as above !
    - sqlAlchemy, if you need to use sqlAlchemy !
    - PyMongo (and a MongoDB server running)



Unit tested ?
=============

It shall ! (please check tests.py)