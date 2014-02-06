### Tells Guardian what kind of framework you are using, supported fw are Flask and Tornado
FRAMEWORK = ''

### Used only with Flask/or Tornado frameworks - this should be changed, of course !
SESSION_SECRET = 'this is my secret key'

### Here must be set the active connection to the database
G_DATABASE_POINTER = None

### default redirect route/URL
REDIRECT_URI = 'login'

### Default dbAdapter, list is sqlite3, sqlAlchemy, pymongo
G_MODEL = 'sqlite3'

### Default sessionAdapter, list is dict, Flask, tornado
G_SESSION = 'dict'

###
DEBUG = True