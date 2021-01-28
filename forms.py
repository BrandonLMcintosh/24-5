from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired, Length
from wtforms.widgets.core import TextArea

class Login_Form(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(max=50)])
    password = PasswordField(validators=[InputRequired()])

class Register_Form(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(max=50)])
    username = StringField(validators=[Length(max=20), InputRequired()])
    password = StringField(validators=[InputRequired()])
    first_name = StringField(validators=[Length(max=30), InputRequired()])
    last_name = StringField(validators=[Length(max=30), InputRequired()])

class Feedback_Form(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(max=100)])
    content = TextAreaField(validators=[InputRequired()])