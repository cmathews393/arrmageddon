from flask import render_template
from app.modules.spotiplex import spotiplex_bp

@spotiplex_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@spotiplex_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
