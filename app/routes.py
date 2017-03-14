from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from .db import db, Entry, User

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('entries.html', entries=entries)

@routes.route('/add', methods=['POST'])
def add_entry():

    template =  request.form['template']
    description = request.form['description']
    if template and description:
        entry = Entry(description=request.form['description'], template=request.form['template'])
        db.session.add(entry)
        db.session.commit()
    else:
        flash("enter a description and template")
    return redirect(url_for('routes.show_entries'))

@routes.route('/delete', methods=['POST'])
def delete_entry():
    Entry.query.delete()
    db.session.commit()
    flash("all entries deleted")
    return redirect(url_for('routes.show_entries'))
