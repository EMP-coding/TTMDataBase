from flask import Blueprint

tee_times_bp = Blueprint('tee_times', __name__)

from . import routes