from flask import render_template

from app.modules.spotiplex import spotiplex_bp


@spotiplex_bp.route("/sync")
def sync():
    return render_template("sync.html.j2")


@spotiplex_bp.route("/settings")
def settings():
    spotiplex_fields = [
        {
            "name": "Spotify Client ID",
            "type": "text",
            "value": "your_spotify_client_id",
        },
        {
            "name": "Spotify Client Secret",
            "type": "text",
            "value": "your_spotify_client_secret",
        },
        {"name": "Plex Token", "type": "text", "value": "your_plex_token"},
    ]
    return render_template(
        "settings.html.j2", fields=spotiplex_fields, service_name="Spotiplex"
    )
