from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo

class LogginForm(Form):
    name = StringField('Username:', validators=[Required()])
    # need to flesh out user password functionality
    password = PasswordField('Password:', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class SignUpForm(Form):
    name = StringField('Choose a user name:', validators=[Required()])
    password = PasswordField('Password:')
    password_confirm = PasswordField('Type your password again:', validators=[EqualTo('password', message="Passwords must match")])
    institution = StringField('Institution where you work (optional):')
    submit = SubmitField('Sign up')

class AddEntryForm(Form):
    #title = StringField('Title:', validators=[Required()])
    description = StringField('Smartphrase Description:', validators=[Required()])
    template = TextAreaField('Smartphrase Template:', validators=[Required()])
    submit = SubmitField('Submit Smartphrase')
