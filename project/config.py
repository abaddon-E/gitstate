class DefaultConfig(object):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@127.0.0.1/flask'
    SECRET_KEY = '@Secret@'
    
    INSTALLED_BLUEPRINTS = (
        'repo',
        'developers',
        'users',
    )
    DEBUG = True
