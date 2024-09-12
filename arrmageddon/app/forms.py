from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange


class SpotifyForm(FlaskForm):
    api_key = StringField("Spotify API Key", validators=[DataRequired()])
    submit = SubmitField("Save Spotify")


class PlexForm(FlaskForm):
    api_key = StringField("Plex API Key", validators=[DataRequired()])
    submit = SubmitField("Save Plex")


class ReadarrForm(FlaskForm):
    api_key = StringField("Readarr API Key", validators=[DataRequired()])
    api_url = StringField("Readarr API URL", validators=[DataRequired()])
    submit = SubmitField("Save Readarr")


class LidarrForm(FlaskForm):
    api_key = StringField("Lidarr API Key", validators=[DataRequired()])
    submit = SubmitField("Save Lidarr")


class AudiobookshelfForm(FlaskForm):
    api_key = StringField("Audiobookshelf API Key", validators=[DataRequired()])
    api_url = StringField("Audiobookshelf API URL", validators=[DataRequired()])
    library_id = StringField("Audiobookshelf Library ID", validators=[DataRequired()])
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


class TagSyncForm(FlaskForm):
    tag = SelectField("Select Tag", validators=[DataRequired()])
    submit = SubmitField("Run Sync")


class TagSelectionForm(FlaskForm):
    tag = SelectField("Select Tag", validators=[DataRequired()], choices=[])
    submit = SubmitField("Load Books")


class BookSyncForm(FlaskForm):
    readarr_book_id = HiddenField("Readarr Book ID")
    abs_book_id = SelectField(
        "Audiobookshelf Book",
        validators=[DataRequired()],
        choices=[],
    )
    sync = SubmitField("Sync")
