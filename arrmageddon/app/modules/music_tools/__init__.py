from flask import Blueprint

music_tools_bp = Blueprint("music_tools", __name__)

from arrmageddon.app.modules.music_tools import routes
