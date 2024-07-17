from flask import flash, redirect, render_template, url_for

from app.forms import AudiobookshelfForm, LidarrForm, PlexForm, ReadarrForm, SpotifyForm
from app.main import main_bp


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("home.html.j2")


@main_bp.route("/settings", methods=["GET", "POST"])
def settings():
    spotify_form = SpotifyForm()
    plex_form = PlexForm()
    readarr_form = ReadarrForm()
    lidarr_form = LidarrForm()
    audiobookshelf_form = AudiobookshelfForm()

    if spotify_form.validate_on_submit() and spotify_form.submit.data:
        # Process Spotify form data here
        flash("Spotify settings saved successfully.", "success")
        return redirect(url_for("main.settings"))

    if plex_form.validate_on_submit() and plex_form.submit.data:
        # Process Plex form data here
        flash("Plex settings saved successfully.", "success")
        return redirect(url_for("main.settings"))

    if readarr_form.validate_on_submit() and readarr_form.submit.data:
        # Process Readarr form data here
        flash("Readarr settings saved successfully.", "success")
        return redirect(url_for("main.settings"))

    if lidarr_form.validate_on_submit() and lidarr_form.submit.data:
        # Process Lidarr form data here
        flash("Lidarr settings saved successfully.", "success")
        return redirect(url_for("main.settings"))

    if audiobookshelf_form.validate_on_submit() and audiobookshelf_form.submit.data:
        # Process Audiobookshelf form data here
        flash("Audiobookshelf settings saved successfully.", "success")
        return redirect(url_for("main.settings"))

    return render_template(
        "settings.html.j2",
        spotify_form=spotify_form,
        plex_form=plex_form,
        readarr_form=readarr_form,
        lidarr_form=lidarr_form,
        audiobookshelf_form=audiobookshelf_form,
    )
