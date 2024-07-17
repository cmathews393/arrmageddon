from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    Bootstrap5(app)
    csrf = CSRFProtect(app)

    from app.main import main_bp
    from app.modules.lidarr import lidarr_bp
    from app.modules.readarr import readarr_bp
    from app.modules.spotiplex import spotiplex_bp
    from arrmageddon.app.modules.music_tools import music_tools_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(music_tools_bp, url_prefix="/music_tools")
    app.register_blueprint(readarr_bp, url_prefix="/readarr")
    app.register_blueprint(lidarr_bp, url_prefix="/lidarr")
    app.register_blueprint(spotiplex_bp, url_prefix="/spotiplex")

    return app
