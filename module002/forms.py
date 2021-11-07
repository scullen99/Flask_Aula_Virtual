from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField#, DateField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
import datetime

class PostForm(FlaskForm):
    body = StringField("Create a new post", validators=[InputRequired()])

class HideForm(FlaskForm):
    name = StringField('Hide')