from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session
from .db import db, Entry, User

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def show_landing():
    session['logged_in'] = False
    # can't fucking connect to this
    print(url_for('static', filename='styles.css'))
    return render_template('landing.html')

@routes.route('/log_out')
def log_out():
    session['logged_in'] = False
    flash("you were logged out")
    return redirect(url_for('routes.show_landing'))

@routes.route('/log_in', methods=['GET', 'POST'])
def show_log_in():
    current_users = [user[0] for user in db.session.query(User.name).all()]
    if request.method == "POST":
        username = request.form['username']
        if username in current_users:
            session['logged_in'] = True
            user = User.query.filter(User.name == username).one()

            # assigning the object gives an error
            session["user"] = username

            return redirect(url_for("routes.show_entries"))
        else:
            flash("you need to sign up")
    return render_template('log_in.html')

@routes.route('/sign_up', methods=['GET', 'POST'])
def show_sign_up():
    if request.method == "POST":
        username = request.form['username']
        institution = request.form['institution']
        current_users = [user[0] for user in db.session.query(User.name).all()]

        # why coudln't i do if not username and institution: (like below)
        if  len(username) == 0 or len(institution) == 0:
            flash('enter both a username and institution')
            return render_template('sign_up.html')

        elif username not in current_users:
            new_user = User(name=username, institution=institution)
            db.session.add(new_user)
            db.session.commit()
            flash("sign up successful")
            session["logged_in"] = True
            session["user"] = new_user.name
            return redirect(url_for("routes.show_entries"))

        else:
            flash("username already in database - choose something else")
            return render_template('sign_up.html')
    else:
        return render_template('sign_up.html')

@routes.route('/show_entries')
def show_entries():
    entries = Entry.query.all()
    if session['logged_in'] == True:
        print("loggin status: ", True)
        return render_template('entries_with_add.html', entries=entries)
    else:
        print(False)
    return render_template('entries.html', entries=entries)

@routes.route('/add', methods=['POST'])
def add_entry():
    template =  request.form['template']
    description = request.form['description']
    user = User.query.filter(User.name == session['user']).one()
    print(user)
    if template and description:
        entry = Entry(description=request.form['description'], template=request.form['template'], user=user)
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
