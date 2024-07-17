from flask import Blueprint

lidarr_bp = Blueprint('lidarr', __name__)

from app.modules.lidarr import routes
