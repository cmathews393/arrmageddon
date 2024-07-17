from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


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


class MusicForm(FlaskForm):
    testbutton = StringField("IDK", validators=[DataRequired()])
    submit = SubmitField("SubmitRun")
