from flask import Flask, render_template, redirect, url_for, request, flash
from .factory import create_app
from .db import db, Entries, Users

app = create_app(__name__)

@app.route('/')
def show_entries():
    entries = Entries.query.all()
    return render_template('entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = Entries(description=request.form['description'], template=request.form['template'])
    print(entry)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('show_entries'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    Entries.query.delete()
    db.session.commit()
    flash("all entries deleted")
    return redirect(url_for('show_entries'))
