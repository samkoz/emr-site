from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# change this to singular
class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=False)
    template = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    #user = db.relationship("User", back_populates="submissions")

    def __repr__(self):
        return "Entry: <description> {}, <template> {}".format(self.description, self.template)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    submissions = db.relationship('Entry', order_by=Entry.id, backref=db.backref('user'))

    def __repr__(self):
        return "User: <name> {}, <institution> {}".format(self.name, self.institution)

    @staticmethod
    def num_submissions(self):
        return(len(self.submissions))
