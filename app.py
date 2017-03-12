from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from entries import entries

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\samko\\OneDrive\\Documents\\Programming\\Projects\\epic_smart_phrases\\test.db'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), unique=False)
    template = db.Column(db.Text(), unique=True)

    def __init__(self, description, template):
        self.description = description
        self.template = template

    def __repr__(self):
        return "Entry:\nDescription: {}\nTemplate: {}\n\n".format(self.description, self.template)

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



# @app.route('/add', methods=['POST'])
# def add_entry():
#     # session was imported above
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     # what does request.form do?
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     # what does this do?
#     flash('New entry was successfully posted')
#     # so you can redirect to the show_entries function, interesting
#     return redirect(url_for('show_entries'))
