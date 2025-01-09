from wtforms import Form, BooleanField, StringField, PasswordField, validators, EmailField, DateField, IntegerField, \
    RadioField, TextAreaField
from wtforms.validators import InputRequired


class RegisterPersonalInformation(Form):
    first_name = StringField('first_name', [validators.Length(min=3, max=50), validators.DataRequired()])
    last_name = StringField('last_name', [validators.Length(min=3, max=50), validators.DataRequired()])
    date_of_birth = DateField('date_of_birth', format="%Y-%m-%d")
    gender = RadioField('gender', choices=['Male', 'Female'], validators=[InputRequired()])
    mobile_no = IntegerField('mobile_no', [validators.DataRequired()])
    email = EmailField('email', [validators.Length(min=3, max=50), validators.Email(), validators.DataRequired()])
    bio = TextAreaField('bio', [validators.Length(min=4), validators.DataRequired()])
    password = PasswordField("password",[validators.Length(min=6, max=30), validators.DataRequired()])
    confirm_password  = PasswordField("confirm_password",[validators.EqualTo('password')])
    privacy = BooleanField('Agree?')


class EditPersonalInformation(Form):
    first_name = StringField('first_name', [validators.Length(min=3, max=50), validators.DataRequired()])
    last_name = StringField('last_name', [validators.Length(min=3, max=50), validators.DataRequired()])
    date_of_birth = DateField('date_of_birth', format="%Y-%m-%d")
    gender = RadioField('gender', choices=['Male', 'Female'], validators=[InputRequired()])
    mobile_no = IntegerField('mobile_no', [validators.DataRequired()])
    email = EmailField('email', [validators.Length(min=3, max=50), validators.Email(), validators.DataRequired()])
    bio = TextAreaField('bio', [validators.Length(min=4), validators.DataRequired()])