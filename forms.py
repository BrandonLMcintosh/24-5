from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import PasswordField
from wtforms.validators import Email, InputRequired, Length

class Login_Form(FlaskForm):
    email = EmailField(validators=[Email(), InputRequired(), Length(max=50)])
    password = PasswordField(validators=[InputRequired()])

class Register_Form(FlaskForm):
    email = EmailField(validators=[Email(), InputRequired(), Length(max=50)])
    username = StringField(validators=[Length(20), InputRequired()])
    password = StringField(validators=[InputRequired()])
    first_name = StringField(validators=[Length(30), InputRequired()])
    last_name = StringField(validators=[Length(30), InputRequired()])