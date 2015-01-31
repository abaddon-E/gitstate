from sqlalchemy import Column, String, Integer, Model, ForeignKey, DateTime
from sqlalchemy.orm import Relationship


class Repository(Model):
    id = Column(Integer, unique=True)
    repo_name = Column(String, unique=True)
    repo_url = Column(String, unique=True)
    user_id =  Column(Integer, ForeignKey('user.id'))
    commit_id = Relationship('Commit')

    def __repr__(self):
        return '<Repo %s>' % self.repo_name


class User(Model):
    id = Column(Integer, unique=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    repo_id = Relationship('Repository')
    commit_id = Relationship('Commit')

    def __repr__(self):
        return '<User %s>' % self.name


class Commit(Model):
    id = Column(String, unique=True)
    message = Column(String, unique=True)
    timestamp = Column(DateTime)
    repo_id = Column(Integer, ForeignKey('repository.id'))
    author = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Message %s>' % self.message


