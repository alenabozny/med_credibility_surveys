from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import sys
import logging

app = Flask(__name__)
app.secret_key = 'super secret string'
app.config.from_object(Config)
app.static_folder = 'static'


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

from app.admin import bp_admin
app.register_blueprint(bp_admin)

from app import routes, models
