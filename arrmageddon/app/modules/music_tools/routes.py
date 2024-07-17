from flask import flash, redirect, render_template, url_for

from app.forms import PlaylistSyncForm
from arrmageddon.app.modules.music_tools import music_tools_bp


@music_tools_bp.route("/")
def index():
    # # form = MusicForm()
    # if form.validate_on_submit():
    #     return redirect(url_for("music_tools.index"))
    return render_template("music_tools.html.j2")


@music_tools_bp.route("/playlist_sync", methods=["GET", "POST"])
def playlist_sync():
    form = PlaylistSyncForm()
    if form.validate_on_submit() and form.run_sync.data:
        # Process form data and run the sync here
        flash("Playlist sync started successfully.", "success")
        return redirect(url_for("main.playlist_sync"))
    return render_template("playlist_sync.html.j2", playlist_sync_form=form)
