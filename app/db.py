from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String(200), unique=False)
    template = db.Column(db.Text())
    user_saves = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return "Entry: <id: {}, time_created: {}, description: {}, template: {}, user_id: {}".format(self.id, self.time_created, self.description, self.template, self.user_id)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    time_enrolled = db.Column(db.DateTime, default=datetime.now)
    saved_entries = db.Column(db.PickleType())
    submissions = db.relationship('Entry', order_by=Entry.id, backref=db.backref('user'))


    def __repr__(self):
        return """User: <id: {}name: {}, institution: {}, submissions: {}, time_enrolled: {}>""".format(self.id, self.name, self.institution, self.submissions, self.time_enrolled)

    def num_submissions(self):
        return len(self.submissions)
