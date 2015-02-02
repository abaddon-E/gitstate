#! /usr/bin/python
from project import create_app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from project.extentions import sqldb as db

#form manager read models better imported them
from project.apps.repo import models
from project.apps.developers import models
from project.apps.users import models

app = create_app()
manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
