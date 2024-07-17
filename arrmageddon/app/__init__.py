from flask import Flask

from app.main.routes import main_bp


def create_app():
    app = Flask(__name__)
    from flask_bootstrap import Bootstrap5

    Bootstrap5(app)
    app.register_blueprint(main_bp)
    return app
