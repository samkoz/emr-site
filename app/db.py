from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from datetime import datetime

db = SQLAlchemy()


association_table = db.Table('assocation_table',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE")),
                db.Column('entry_id', db.Integer, db.ForeignKey('entries.id', ondelete="CASCADE", onupdate="CASCADE")),
                )

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200), unique=False)
    template = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __repr__(self):
        return_string = "Entry Object:\n"
        var_dict = self.__dict__
        for k in var_dict.keys():
            if k == "user_saves":
                return_string += "{}: {}\n".format(k, len(self.user_saves))
            elif k == "user":
                 return_string += "{}: {}\n".format(k, self.user.id)
            elif k != "_sa_instance_state":
                return_string += "{}: {}\n".format(k, var_dict[k])
        return return_string

    def num_user_saves(self):
        return len(self.user_saves)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), default="password")
    institution = db.Column(db.String(200), default=None)
    time_enrolled = db.Column(db.DateTime, default=datetime.utcnow)
    saved_entries = db.relationship("Entry", secondary=association_table, backref=db.backref("user_saves"))
    submissions = db.relationship('Entry', order_by=Entry.id, backref=db.backref('user'))

    def __repr__(self):
        return_string = "User Object:\n"
        var_dict = self.__dict__
        for k in var_dict.keys():
            if k =="saved_entries":
                return_string += "{}: {}\n".format(k, len(self.saved_entries))
            elif k == "submissions":
                return_string += "{}: {}\n".format(k, len(self.submissions))
            elif k != "_sa_instance_state":
                return_string += "{}: {}\n".format(k, var_dict[k])
        return return_string

    @property
    def url(self):
        return url_for('.view_profile', username=self.name)

    def num_submissions(self):
        return len(self.submissions)

    def num_saved_entries(self):
        return len(self.saved_entries)
