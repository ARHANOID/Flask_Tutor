from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Wrong email, try again")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100, message="Wrong psw")])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Enter")

class RegisterForm(FlaskForm):
    name = StringField("name: ", validators=[DataRequired(), Length(min=3, max=100, message="Name is too short")])
    email = StringField("Email: ", validators=[Email("Wrong email, try again")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=3, max=100, message="password is too short")])
    psw2 = PasswordField("Confirm password: ", validators=[DataRequired(), EqualTo("psw", message="passwords doesn't match")])
    age = StringField("age: ", validators=[DataRequired(), Length(min=1, max=150, message="Name is too short")])
    city = StringField("city: ", validators=[DataRequired(), Length(min=1, max=150, message="Name is too short")])



    submit = SubmitField("Register")
