from flask import render_template
from app.modules.readarr import readarr_bp

@readarr_bp.route('/sync')
def sync():
    return render_template('sync.html.j2')

@readarr_bp.route('/settings')
def settings():
    return render_template('settings.html.j2')
