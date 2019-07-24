from flask import Blueprint

bp = Blueprint('main', __name__)

# Bootstrap the database
from app import bootstrap_db

from app.main import routes
