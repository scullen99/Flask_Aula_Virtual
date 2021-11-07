from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField, TextAreaField#, DateField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
from flask_wtf.file import FileField
import datetime

class AssigmentForm(FlaskForm):
    name = StringField('Assignment title',validators=[InputRequired()])
     #descripcion = StringField("Create a new assignment", validators=[InputRequired()], widget=TextArea())
    never_expire = BooleanField('Never expire')
    date_expire = DateField('Choose an expiring date',format='%Y-%m-%d', default=datetime.datetime.today)
    time_expire = TimeField('Expiring time',format='%H:%M', default=datetime.time(23, 59))
    descripcion = TextAreaField('Assigment description')

class GradesForm(FlaskForm):
    name = StringField('Grade',validators=[InputRequired()])

class DownloadForm(FlaskForm):
    name = StringField('Download')


