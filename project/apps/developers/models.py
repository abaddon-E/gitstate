from project.extentions import sqldb as db
from sqlalchemy.orm import relationship


class Developer(db.Model):
    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    repo_id = relationship('Repository')
    commit_id = relationship('Commit')

    def __repr__(self):
        return '<Developer %s>' % self.name
