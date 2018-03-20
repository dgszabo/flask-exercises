from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from project.models import User

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min = 8, max = 20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min = 8, max = 20)])