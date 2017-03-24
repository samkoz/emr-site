from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class LogginForm(Form):
    name = StringField('Username:', validators=[Required()])
    submit = SubmitField('Log in')

class SignUpForm(Form):
    name = StringField('Choose a user name:', validators=[Required()])
    institution = StringField('Institution where you work (optional):')
    submit = SubmitField('Sign up')

class AddEntryForm(Form):
    #title = StringField('Title:', validators=[Required()])
    description = StringField('Smartphrase Description:', validators=[Required()])
    template = TextAreaField('Smartphrase Template:', validators=[Required()])
    submit = SubmitField('Submit Smartphrase')
