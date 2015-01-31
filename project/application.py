from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

DEFAULT_APP_NAME = 'project'


def create_app(app_name=DEFAULT_APP_NAME):
    app = Flask(
        app_name,
        static_folder='media/statics/',
        template_folder='media/templates',
        static_url_path='')
    app.config.from_object('config')
    configure_blueprints(app)
    db = SQLAlchemy(app)
    Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    configure_blueprints(app)
    return manager


def configure_blueprints(app):

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:
        bp = __import__('project.apps.%s' % blueprint_name, fromlist=['views'])

        try:
            mod = __import__('project.%s' % blueprint_name, fromlist=['urls'])
        except ImportError:
            pass
        else:
            mod.urls.add_url_rules(bp.views.mod)
        try:
            app.register_blueprint(bp.views.mod)
        except:
            # report has no views
            pass
