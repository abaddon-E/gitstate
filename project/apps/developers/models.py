from project.extentions import sqldb as db
from sqlalchemy.orm import relationship


class Developer(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    repo_id = relationship('Repository')
    commit_id = relationship('Commit')

    def __repr__(self):
        return '<Developer %s>' % self.name
