from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://newuser:password@localhost/epic_smart_phrases'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=False)
    template = db.Column(db.Text())

    def __init__(self, description, template):
        self.description = description
        self.template = template

    def __repr__(self):
        return "Entry:\nDescription: {}\nTemplate: {}\n".format(self.description, self.template)

@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = Entry(request.form['description'], request.form['template'])
    print(entry)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('show_entries'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    Entry.query.delete()
    db.session.commit()
    flash("all entries deleted")
    return redirect(url_for('show_entries'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    db.create_all()
