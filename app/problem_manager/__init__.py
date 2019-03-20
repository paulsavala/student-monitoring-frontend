from flask import Blueprint

bp = Blueprint('problem_manager', __name__)

from app.problem_manager import routes