class DefaultConfig(object):
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://U:P@127.0.0.1/DB'
    SECRET_KEY = '@Secret@'
    
    INSTALLED_BLUEPRINTS = (
        'PUSH_EVENT',
    )
