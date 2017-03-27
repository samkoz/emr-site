from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

specialties = ['Cardiology',
    'Critical Care/ICU',
    'Dermatology',
    'Emergency Medicine',
    'ENT',
    'Family Medicine',
    'Gastroenterology',
    'General Internal Medicine',
    'Hematology/Oncology',
    'Nephrology',
    'Neurology',
    'Neurosurgery',
    'Obstetrics/Gynecology',
    'Ophthalmology',
    'Pediatrics',
    'Psychiatry',
    'Pulmonology',
    'Radiology',
    'Surgery: Colorectal',
    'Surgery:General',
    'Surgery: Transplant',
    'Transplant',
    'Urology']

note_type = ['Code/Rapid Response',
    'Care Conference',
    'Consult',
    'Discharge Summary',
    'H&P',
    'Operation Note',
    'Progress Note',
    'Proccedure Note']

note_part = ['Lab Results',
    'HPI',
    'ROS',
    'Physical Exam',
    'Past Medical History',
    'Surgical History',
    'Family History',
    'Social Hx',
    'Medications',
    'Assessment and Plan']

all_tags = specialties + note_type + note_part

association_table = db.Table('assocation_table',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE")),
                db.Column('entry_id', db.Integer, db.ForeignKey('entries.id', ondelete="CASCADE", onupdate="CASCADE")),
                )

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(10000), unique=False)
    template = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"))
    num_user_saves = db.Column(db.Integer(), default=0)
    tags = db.Column(db.String(1000))

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

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        from random import sample
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, 10)).first()
            p = Entry(description=forgery_py.lorem_ipsum.title(words_quantity=4),
                template=forgery_py.lorem_ipsum.sentences(50),
                time_created=forgery_py.date.date(True),
                tags=', '.join(sample(all_tags, 4)),
                user=u)
            db.session.add(p)
            db.session.commit()

    @property
    def too_long(self):
        template = self.template
        if len(template) / 100  + template.count('\n') + 1 > 7:
            return True
        else:
            return False

    @property
    def template_display(self):
        if self.too_long:
            new_lines_split = self.template.split('\n')
            remaining_lines = 7
            shortened_template = []
            for line in new_lines_split:
                if remaining_lines < 0:
                    break
                current_new_lines = (len(line) / 100) + 1
                print(current_new_lines)
                if current_new_lines > 7:
                    shortened_template.append(line[:700])
                else:
                    shortened_template.append(line)
                remaining_lines -= current_new_lines
                print(remaining_lines)
            shortened_template = '\n'.join(shortened_template)
            return shortened_template
        else:
            return self.template



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    password_hash = db.Column(db.String(1000))
    specialty = db.Column(db.String(1000))
    profession = db.Column(db.String(1000))
    institution = db.Column(db.String(1000), default=None)
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

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        import forgery_py

        seed()
        for i in range(count):
            u = User(name=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word(),
                institution=forgery_py.address.city(),
                time_enrolled=forgery_py.date.date(True),
                profession=choice(['Physician', 'Nurse Practitionar', 'Physician Assistant']),
                specialty=choice(specialties)
                )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def url(self):
        return url_for('.view_profile', username=self.name)

    def num_submissions(self):
        return len(self.submissions)

    def num_saved_entries(self):
        return len(self.saved_entries)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
