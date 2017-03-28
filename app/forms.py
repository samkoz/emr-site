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
    profession = RadioField('Profession:', choices=[
        ('Physician', 'Physician'),
        ('Nurse Practitioner', 'Nurse Practitioner'),
        ('Physician\'s Assistant', 'Physicians\'s Assistant')], validators=[Required()])
    specialty = StringField('Specialty (if applicable):')
    institution = StringField('Institution where you work (optional):')
    submit = SubmitField('Sign up')

class AddEntryForm(Form):
    #title = StringField('Title:', validators=[Required()])
    description = StringField('Smartphrase Description:', validators=[Required(), Length(max=200)])
    template = TextAreaField('Smartphrase Template:', validators=[Required(), Length(max=65534)])
    specialty = SelectMultipleField('Specialty', choices=[
        ('Cardiology', 'Cardiology'),
        ('Critical Care/ICU', 'Critical Care/ICU'),
        ('Dermatology', 'Dermatology'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('ENT', 'ENT'),
        ('Family Medicine', 'Family Medicine'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General Internal Medicine', 'General Internal Medicine'),
        ('Hematology/Oncology', 'Hematology/Oncology'),
        ('Nephrology', 'Nephrology'),
        ('Neurology', 'Neurology'),
        ('Neurosurgery', 'Neurosurgery'),
        ('Obstetrics/Gynecology', 'Obstetrics/Gynecology'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Pulmonology', 'Pulmonology'),
        ('Radiology', 'Radiology'),
        ('Surgery: Colorectal', 'Surgery: Colorectal'),
        ('Surgery: General', 'Surgery: General'),
        ('Surgery: Transplant', 'Surgery: Transplant'),
        ('Transplant', 'Transplant'),
        ('Urology', 'Urology')
        ])
    note_type = SelectMultipleField('Note Type', choices=[
        ('Code/Rapid Response', 'Code/Rapid Response'),
        ('Care Conference', 'Care Conference'),
        ('Consult', 'Consult'),
        ('Discharge Summary', 'Discharge Summary'),
        ('H&P', 'H&P'),
        ('Operation Note', 'Operation Note'),
        ('Progress Note', 'Progress Note'),
        ('Proccedure Note', 'Procedure Note')
        ])
    note_part = SelectMultipleField('Note Component', choices=[
        ('Miscellaneous', 'Miscellaneous'),
        ('Lab Results', 'Lab Results'),
        ('HPI', 'HPI'),
        ('ROS', 'ROS'),
        ('Physical Exam', 'Physical Exam'),
        ('Past Medical History', 'Past Medical History'),
        ('Surgical History', 'Surgical History'),
        ('Family History', 'Family History'),
        ('Social Hx', 'Social Hx'),
        ('Medications', 'Medications'),
        ('Assessment and Plan', 'Assessment and Plan')
    ])
    remember_tags = BooleanField('Remember Tags')
    submit = SubmitField('Submit Smartphrase')

class SearchForm(Form):
    search_order = RadioField('Order search results by', choices=[
        ('submission_time', 'Most recent'),
        ('saves', 'Most saved')], validators=[Required()])
    search_query = StringField('Search')
    specialty = SelectMultipleField('Specialty', choices=[
        ('Cardiology', 'Cardiology'),
        ('Critical Care/ICU', 'Critical Care/ICU'),
        ('Dermatology', 'Dermatology'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('ENT', 'ENT'),
        ('Family Medicine', 'Family Medicine'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General Internal Medicine', 'General Internal Medicine'),
        ('Hematology/Oncology', 'Hematology/Oncology'),
        ('Nephrology', 'Nephrology'),
        ('Neurology', 'Neurology'),
        ('Neurosurgery', 'Neurosurgery'),
        ('Obstetrics/Gynecology', 'Obstetrics/Gynecology'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Pulmonology', 'Pulmonology'),
        ('Radiology', 'Radiology'),
        ('Surgery: Colorectal', 'Surgery: Colorectal'),
        ('Surgery: General', 'Surgery: General'),
        ('Surgery: Transplant', 'Surgery: Transplant'),
        ('Transplant', 'Transplant'),
        ('Urology', 'Urology')
        ])
    note_type = SelectMultipleField('Note Type', choices=[
        ('Code/Rapid Response', 'Code/Rapid Response'),
        ('Care Conference', 'Care Conference'),
        ('Consult', 'Consult'),
        ('Discharge Summary', 'Discharge Summary'),
        ('H&P', 'H&P'),
        ('Operation Note', 'Operation Note'),
        ('Progress Note', 'Progress Note'),
        ('Proccedure Note', 'Procedure Note')

        ])
    note_part = SelectMultipleField('Note Component', choices=[
        ('Miscellaneous', 'Miscellaneous'),
        ('Lab Results', 'Lab Results'),
        ('HPI', 'HPI'),
        ('ROS', 'ROS'),
        ('Physical Exam', 'Physical Exam'),
        ('Past Medical History', 'Past Medical History'),
        ('Surgical History', 'Surgical History'),
        ('Family History', 'Family History'),
        ('Social Hx', 'Social Hx'),
        ('Medications', 'Medications'),
        ('Assessment and Plan', 'Assessment and Plan')
    ])
    submit = SubmitField('Search')

class UserProfileToggle(Form):
    display_type = RadioField(choices=[('Submitted', 'Submitted Entries'), ('Saved', 'Saved Entries')], default='Submitted')
    submit = SubmitField('Display')
