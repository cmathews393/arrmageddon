from flask import Blueprint

spotiplex_bp = Blueprint("spotiplex", __name__)

from arrmageddon.app.modules.spotiplex import routes
