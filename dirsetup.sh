#!/bin/bash

BASE_DIR="app/modules"

# Create necessary directories if they don't exist
mkdir -p $BASE_DIR/readarr
mkdir -p $BASE_DIR/lidarr
mkdir -p $BASE_DIR/spotiplex

# Create init file for the readarr module
cat <<EOL > $BASE_DIR/readarr/__init__.py
from flask import Blueprint

readarr_bp = Blueprint('readarr', __name__)

from app.modules.readarr import routes
EOL

# Create routes file for the readarr module
cat <<EOL > $BASE_DIR/readarr/routes.py
from flask import render_template
from app.modules.readarr import readarr_bp

@readarr_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@readarr_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
EOL

# Create init file for the lidarr module
cat <<EOL > $BASE_DIR/lidarr/__init__.py
from flask import Blueprint

lidarr_bp = Blueprint('lidarr', __name__)

from app.modules.lidarr import routes
EOL

# Create routes file for the lidarr module
cat <<EOL > $BASE_DIR/lidarr/routes.py
from flask import render_template
from app.modules.lidarr import lidarr_bp

@lidarr_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@lidarr_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
EOL

# Create init file for the spotiplex module
cat <<EOL > $BASE_DIR/spotiplex/__init__.py
from flask import Blueprint

spotiplex_bp = Blueprint('spotiplex', __name__)

from app.modules.spotiplex import routes
EOL

# Create routes file for the spotiplex module
cat <<EOL > $BASE_DIR/spotiplex/routes.py
from flask import render_template
from app.modules.spotiplex import spotiplex_bp

@spotiplex_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@spotiplex_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
EOL

# Update the main __init__.py to register the blueprints
cat <<EOL > app/__init__.py
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
EOL

echo "Blueprints and routes have been set up in the modules folder."
