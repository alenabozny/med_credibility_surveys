from app import db
from datetime import date
import enum

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.Date)
    access_date = db.Column(db.Date, default=date.today())
    url = db.Column(db.String(150))
    title = db.Column(db.String(150))
    query = db.Column(db.String(100))

    def __repr__(self):
        return '<Article "{}".'.format(self.title)


class Sentence(db.Model):
    sentence_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    article_id = db.Column(db.Integer, db.ForeignKey('article.article_id'))
    sequence_nr = db.Column(db.Integer) # position in the article
    to_evaluate = db.Column(db.Boolean)

    def __repr__(self):
        return '<Sentence "{}" from article {}.>'.format(self.body, self.article_id)


class CredibilityRates(enum.Enum):
    CRED = "credible"
    NONCRED = "noncredible"
    NEU = "neutral/irrelevant"

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.sentence_id'), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    rate = db.Column(db.Enum(CredibilityRates))
