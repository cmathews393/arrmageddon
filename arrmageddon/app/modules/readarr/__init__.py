from flask import Blueprint

readarr_bp = Blueprint("readarr", __name__)

from arrmageddon.app.modules.readarr import routes
