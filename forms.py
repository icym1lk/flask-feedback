from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
import email_validator

class UserDetailsForm(FlaskForm):
    """Form for registering users and users details page."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Must be 20 characters or less")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50, message="Must be 50 characters or less")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30, message="Must be between 1 and 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30, message="Must be between 1 and 30 characters")])

class LoginUserForm(FlaskForm):
    """Form for registering users."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Must be 20 characters or less")])
    password = PasswordField("Password", validators=[InputRequired()])

class AddFeedbackForm(FlaskForm):
    """Form for adding feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Must be less than 100 characters")])
    content = TextField("Content", validators=[InputRequired()])