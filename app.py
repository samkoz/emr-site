from flask import Flask, render_template, redirect, url_for, request
from entries import entries

app = Flask(__name__)

app.config.from_object(__name__)

@app.route('/')
def show_entries():
    return render_template('entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entries.append({"description" : request.form['description'], "template" : request.form['template']})
    print(entries)
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
