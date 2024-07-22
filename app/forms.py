from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    location = SelectField('Location', choices=[('location1', 'Location 1'), ('location2', 'Location 2')])
    file = FileField('Upload CSV', validators=[DataRequired()])
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    location = SelectField('Location', choices=[('all', 'All')] + [(loc, loc) for loc in ['location1', 'location2']])
    search = StringField('Search')
    submit = SubmitField('Search')
