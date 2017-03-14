from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session
from .db import db, Entry, User

routes = Blueprint('routes', __name__, template_folder='templates')

# signed_up_users = [user.name for user in User.query.all()]
# def update_user

@routes.route('/')
def show_landing():
    print(url_for('static', filename='styles.css'))
    return render_template('landing.html')

@routes.route('/log_in', methods=['GET', 'POST'])
def show_log_in():
    # # test:
    # user = User(name="Sam", institution="UofMN")
    # db.session.add(user)
    # db.session.commit()
    # users = db.session.query(User.name).all()
    # signed_up_users = [user[0] for user in users]
    # print(signed_up_users)
    # print("Sam" in signed_up_users)
    # User.query.delete()
    # db.session.commit()
    current_users = [user[0] for user in db.session.query(User.name).all()]
    if request.method == "POST":
        if request.form['username'] in current_users:
            session['logged_in'] = True
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

@routes.route('/add_entries')
def show_add_entry():
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
