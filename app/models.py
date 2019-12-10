from app import db
from datetime import date
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='user')

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_password_correct(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username


class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.Date)
    access_date = db.Column(db.Date, default=date.today())
    url = db.Column(db.String(150))
    title = db.Column(db.String(150))
    queryTxt = db.Column(db.String(100))
    keywords = db.Column(db.String(200))
    sentences = db.relationship('Sentence', backref='article')

    def __repr__(self):
        return '<Article "{}">'.format(self.title)


# decorator for the class function
def handle_nonexistent(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return ""

    return wrapper


# class ModificationTypes(enum.Enum):
#     HEDGE = "hedging"
#     AHEDGE = "antihedging"
#     NEG = "negation"
#     HYPER = "hyperonymy"
#     HYPO = "hyponymy"
#     SYN = "synonymy"


class Sentence(db.Model):
    sentence_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    article_id = db.Column(db.Integer, db.ForeignKey('article.article_id'))
    sequence_nr = db.Column(db.Integer)  # position in the article
    to_evaluate = db.Column(db.Boolean)
    task = db.relationship('Task', backref='sentence')
    modification = db.Column(db.String(20))

    @handle_nonexistent
    def get_left_context(self, iterator):
        return Sentence.query.filter_by(
            sequence_nr=self.sequence_nr - iterator,
            article_id=self.article_id) \
            .first().body

    @handle_nonexistent
    def get_right_context(self, iterator):
        return Sentence.query.filter_by(
            sequence_nr=self.sequence_nr + iterator,
            article_id=self.article_id) \
            .first().body

    def get_context_sentences(self):
        sents = Sentence.query.filter_by(article_id=self.article_id)
        seq_nr = self.sequence_nr
        left_length = len(sents[:seq_nr - 1])
        right_length = len(sents[seq_nr:])
        len_range = left_length if left_length > right_length else right_length
        context_dict = {}

        for i in range(1, len_range + 1):
            left_context = self.get_left_context(i)
            right_context = self.get_right_context(i)

            context_dict[i] = {'left': left_context, 'right': right_context}

        return context_dict

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
    steps = db.Column(db.Integer)
    tags = db.Column(db.String(200))
    reason = db.Column(db.String(200))

    def __repr__(self):
        return '<Task for sentence "{}" from article {}.>'.format(self.sentence.body, self.sentence.article_id)
