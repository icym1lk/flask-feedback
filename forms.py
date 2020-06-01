from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
import email_validator

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Must be 20 characters or less")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50, message="Must be 50 characters or less")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30, message="Must be between 1 and 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30, message="Must be between 1 and 30 characters")])