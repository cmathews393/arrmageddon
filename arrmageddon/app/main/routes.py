from flask import flash, redirect, render_template, url_for, request

from app.forms import AudiobookshelfForm, LidarrForm, PlexForm, ReadarrForm, SpotifyForm
from app.main import main_bp
from arrmageddon.app.modules.confighandler.main import read_config, write_config


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("home.html.j2")


@main_bp.route("/settings", methods=["GET"])
def settings():
    spotify_form = SpotifyForm()
    plex_form = PlexForm()
    readarr_form = ReadarrForm()
    lidarr_form = LidarrForm()
    audiobookshelf_form = AudiobookshelfForm()

    # Load existing settings to populate the forms
    spotify_settings = read_config("spotify")
    plex_settings = read_config("plex")
    readarr_settings = read_config("readarr")
    lidarr_settings = read_config("lidarr")
    audiobookshelf_settings = read_config("audiobookshelf")

    spotify_form.api_key.data = spotify_settings.get("api_key", "")
    plex_form.api_key.data = plex_settings.get("api_key", "")
    readarr_form.api_key.data = readarr_settings.get("api_key", "")
    readarr_form.api_url.data = readarr_settings.get("api_url", "")
    lidarr_form.api_key.data = lidarr_settings.get("api_key", "")
    audiobookshelf_form.api_key.data = audiobookshelf_settings.get("api_key", "")
    audiobookshelf_form.api_url.data = audiobookshelf_settings.get("api_url", "")
    audiobookshelf_form.library_id.data = audiobookshelf_settings.get("library_id", "")

    return render_template(
        "settings.html.j2",
        spotify_form=spotify_form,
        plex_form=plex_form,
        readarr_form=readarr_form,
        lidarr_form=lidarr_form,
        audiobookshelf_form=audiobookshelf_form,
    )


@main_bp.route("/save_spotify_settings", methods=["POST"])
def save_spotify_settings():
    spotify_form = SpotifyForm()
    if spotify_form.validate_on_submit() and spotify_form.submit.data:
        data = {"api_key": spotify_form.api_key.data}
        write_config("spotify", data)
        flash("Spotify settings saved successfully.", "success")
    return redirect(url_for("main.settings"))


@main_bp.route("/save_plex_settings", methods=["POST"])
def save_plex_settings():
    plex_form = PlexForm()
    if plex_form.validate_on_submit() and plex_form.submit.data:
        data = {"api_key": plex_form.api_key.data}
        write_config("plex", data)
        flash("Plex settings saved successfully.", "success")
    return redirect(url_for("main.settings"))


@main_bp.route("/save_readarr_settings", methods=["POST"])
def save_readarr_settings():
    readarr_form = ReadarrForm()
    if readarr_form.validate_on_submit() and readarr_form.submit.data:
        data = {
            "api_key": readarr_form.api_key.data,
            "api_url": readarr_form.api_url.data,
        }
        write_config("readarr", data)
        flash("Readarr settings saved successfully.", "success")
    return redirect(url_for("main.settings"))


@main_bp.route("/save_lidarr_settings", methods=["POST"])
def save_lidarr_settings():
    lidarr_form = LidarrForm()
    if lidarr_form.validate_on_submit() and lidarr_form.submit.data:
        data = {"api_key": lidarr_form.api_key.data}
        write_config("lidarr", data)
        flash("Lidarr settings saved successfully.", "success")
    return redirect(url_for("main.settings"))


@main_bp.route("/save_audiobookshelf_settings", methods=["POST"])
def save_audiobookshelf_settings():
    audiobookshelf_form = AudiobookshelfForm()
    if audiobookshelf_form.validate_on_submit() and audiobookshelf_form.submit.data:
        data = {
            "api_key": audiobookshelf_form.api_key.data,
            "api_url": audiobookshelf_form.api_url.data,
            "library_id": audiobookshelf_form.library_id.data,
        }
        write_config("audiobookshelf", data)
        flash("Audiobookshelf settings saved successfully.", "success")
    return redirect(url_for("main.settings"))
