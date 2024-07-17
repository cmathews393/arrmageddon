from flask import Blueprint

lidarr_bp = Blueprint("lidarr", __name__)

from arrmageddon.app.modules.lidarr import routes
