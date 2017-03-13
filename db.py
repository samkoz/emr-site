from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entries(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=False)
    template = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('Users', backref=db.backref('entries'))

    def __repr__(self):
        return "Entry:\nDescription: {}\nTemplate: {}\n".format(self.description, self.template)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    submissions = db.relationship('Entries', order_by=Entries.id, backref=db.backref('users'))

    @staticmethod
    def num_submissions(self):
        return(len(self.submissions))
