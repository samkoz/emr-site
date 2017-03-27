from flask_wtf import Form
from flask import request
from wtforms import StringField, SubmitField, TextAreaField, \
    PasswordField, BooleanField, RadioField, SelectMultipleField
from wtforms.validators import Required, EqualTo, Length

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
    specialty = SelectMultipleField('Specialty', choices=[
        ('IM', 'Internal Medicine'),
        ('Peds', 'Pediatrics'),
        ('GenSurg', 'General Surgery')])
    note_type = SelectMultipleField('Note Type', choices=[
        ('HandP', 'H&P'),
        ('Prog', 'Progress Note'),
        ('Proc', 'Procedure Note'),
        ('Op', 'Operation Note')
        ])
    note_part = SelectMultipleField('Note Component', choices=[
        ('HPI', 'HPI'),
        ('ROS', 'ROS'),
        ('SocHx', 'Social History'),
        ('Meds', 'Medications')
    ])
    submit = SubmitField('Submit Smartphrase')

class SearchForm(Form):
    search_order = RadioField('Order search results by', choices=[
        ('submission_time', 'Most recent'),
        ('saves', 'Most saved')], validators=[Required()])
    search_query = StringField('Search')
    specialty = SelectMultipleField('Specialty', choices=[
        ('IM', 'Internal Medicine'),
        ('Peds', 'Pediatrics'),
        ('GenSurg', 'General Surgery')])
    note_type = SelectMultipleField('Note Type', choices=[
        ('HandP', 'H&P'),
        ('Prog', 'Progress Note'),
        ('Proc', 'Procedure Note'),
        ('Op', 'Operation Note')
        ])
    note_part = SelectMultipleField('Note Component', choices=[
        ('HPI', 'HPI'),
        ('ROS', 'ROS'),
        ('SocHx', 'Social History'),
        ('Meds', 'Medications')
    ])
    submit = SubmitField('Search')
