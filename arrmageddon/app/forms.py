from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SpotifyForm(FlaskForm):
    api_key = StringField("Spotify API Key", validators=[DataRequired()])
    submit = SubmitField("Save Spotify")


class PlexForm(FlaskForm):
    api_key = StringField("Plex API Key", validators=[DataRequired()])
    submit = SubmitField("Save Plex")


class ReadarrForm(FlaskForm):
    api_key = StringField("Readarr API Key", validators=[DataRequired()])
    submit = SubmitField("Save Readarr")


class LidarrForm(FlaskForm):
    api_key = StringField("Lidarr API Key", validators=[DataRequired()])
    submit = SubmitField("Save Lidarr")


class AudiobookshelfForm(FlaskForm):
    api_key = StringField("Audiobookshelf API Key", validators=[DataRequired()])
    submit = SubmitField("Save Audiobookshelf")


class PlaylistSyncForm(FlaskForm):
    replace_existing = BooleanField("Replace Existing Playlists")
    pull_cover_art = BooleanField("Pull Cover Art")
    sync_frequency = IntegerField(
        "Sync Frequency (minutes)",
        validators=[NumberRange(min=1, max=1440)],
    )
    run_sync = SubmitField("Run Sync")
    submit = SubmitField("Save Settings")
