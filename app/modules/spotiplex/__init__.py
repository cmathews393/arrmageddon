from flask import Blueprint

spotiplex_bp = Blueprint('spotiplex', __name__)

from app.modules.spotiplex import routes
