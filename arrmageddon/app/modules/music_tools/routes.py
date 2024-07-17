from flask import redirect, render_template, url_for

from app.forms import MusicForm
from arrmageddon.app.modules.music_tools import music_tools_bp


@music_tools_bp.route("/")
def index():
    form = MusicForm()
    if form.validate_on_submit():
        return redirect(url_for("music_tools.index"))
    return render_template("music_tools.html.j2", form=form)
