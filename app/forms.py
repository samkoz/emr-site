from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class LogginForm(Form):
    name = StringField('Username:', validators=[Required()])
    submit = SubmitField('Log in')

class SignUpForm(Form):
    name = StringField('Choose a user name:', validators=[Required()])
    institution = StringField('Institution where you work (optional):')
    submit = SubmitField('Sign up')
