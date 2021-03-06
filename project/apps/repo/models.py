from project.extentions import sqldb as db
from sqlalchemy.orm import relationship


class Repository(db.Model):
    __tablename__ = 'repositories'
        
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, unique=True)
    repo_name = db.Column(db.String(64), unique=True)
    repo_url = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('developers.id'))
    commit_id = relationship('Commit')

    def __repr__(self):
        return '<Repo %s>' % self.repo_name



class Commit(db.Model):
    __tablename__ = 'commit'
    
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String(255), unique=True)
    message = db.Column(db.String(255), unique=True)
    timestamp = db.Column(db.DateTime)
    repo_id = db.Column(db.Integer, db.ForeignKey('repositories.id'))
    author = db.Column(db.Integer, db.ForeignKey('developers.id'))

    def __repr__(self):
        return '<Message %s>' % self.message


