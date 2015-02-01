from project.extentions import sqldb as db
from random import random
from hashlib import md5


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))
    reset_key = db.Column(db.String)
    

    def rst(self):
        code = md5(str(random()))
        self.reset_key = code.hexdigest()
        return self.reset_key
    
    def name_show(self):
        if self.fullname != '':
            name = self.fullname
        else:
            name = self.username
        return name
        
    def __repr__(self):
        return self.name_show
