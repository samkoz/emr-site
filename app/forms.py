from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, EqualTo

class LogginForm(Form):
    name = StringField('Username:', validators=[Required()])
    # need to flesh out user password functionality
    password = StringField('Password:')
    submit = SubmitField('Log in')

class SignUpForm(Form):
    name = StringField('Choose a user name:', validators=[Required()])
    password = StringField('Password:')
    password_confirm = StringField('Type your password again:', validators=[EqualTo('password', message="Passwords must match")])
    institution = StringField('Institution where you work (optional):')
    submit = SubmitField('Sign up')

class AddEntryForm(Form):
    #title = StringField('Title:', validators=[Required()])
    description = StringField('Smartphrase Description:', validators=[Required()])
    template = TextAreaField('Smartphrase Template:', validators=[Required()])
    submit = SubmitField('Submit Smartphrase')
