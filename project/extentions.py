from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

sqldb = SQLAlchemy()


login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = ('Please log in to access this page.')

@login_manager.user_loader
def load_user(id):
   if id:
       from project.apps.user.models import User
       return User.objects.get(id=id)
