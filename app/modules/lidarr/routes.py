from flask import render_template
from app.modules.lidarr import lidarr_bp

@lidarr_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@lidarr_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
