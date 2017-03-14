from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session
from .db import db, Entry, User

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def show_landing():
    print(url_for('static', filename='styles.css'))
    return render_template('landing.html')

@routes.route('/log_in')
def show_log_in():
    return render_template('log_in.html')

@routes.route('/sign_up')
def show_sign_up():
    # if request.form['username'] not in [user.name for user in User.query.all():
    return render_template('sign_up.html')

@routes.route('/show_entries')
def show_entries():
    entries = Entry.query.all()
    return render_template('entries.html', entries=entries)

@routes.route('/add_entries')
def show_add_entry():
    # if session['logged_in'] == True:
    #     pass
    # else:
    return render_template('add_entries.html')

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
