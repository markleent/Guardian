### Tells Guardian what kind of framework you are using - this is useful for things like
FRAMEWORK = ''

### Self explanatory !
USE_SESSION = True

### Used only with Flask/or Tornado frameworks
SESSION_SECRET = ''

### Here must be set the active connection to the database
G_DATABASE_POINTER = None

### default redirect route
REDIRECT_ROUTE = '/login'

### Default dbAdapter
G_MODEL = 'auth.models.sql3Adapter'

### Default sessionAdapter
G_SESSION = 'auth.session.dictAdapter'

