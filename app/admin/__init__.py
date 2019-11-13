from flask import Blueprint

bp_admin = Blueprint('admin', __name__, template_folder='templates', url_prefix="/admin")

from app.admin import routes
