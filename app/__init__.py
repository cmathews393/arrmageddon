from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.main import main_bp
    from app.modules.readarr import readarr_bp
    from app.modules.lidarr import lidarr_bp
    from app.modules.spotiplex import spotiplex_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(readarr_bp, url_prefix='/readarr')
    app.register_blueprint(lidarr_bp, url_prefix='/lidarr')
    app.register_blueprint(spotiplex_bp, url_prefix='/spotiplex')

    return app
