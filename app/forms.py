from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class LogginForm(Form):
    name = StringField('Username:', validators=[Required()])
    submit = SubmitField('Submit')
