from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session, json
from .db import db, Entry, User
from sqlalchemy import desc

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def show_landing():
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

@routes.route('/show_entries', methods=['GET', 'POST'])
# will need to include order here somehow...
def show_entries():
    if request.method == "POST":
        entry_id = int(request.form["entry_id"])

        entry = Entry.query().filter(Entry.id == entry_id)
        entry.num_saves += 1
        db.session.commit()
        return json.dumps({'status':'OK'});
    else:
        entries = Entry.query.order_by(desc(Entry.id)).all()
        print(entries)
        entries = enumerate(entries, 1)
        return render_template('entries.html', entries=entries)

@routes.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == "POST":
        template =  request.form['template']
        description = request.form['description']
        user = User.query.filter(User.name == session['user']).one()
        print(user)
        if template and description:
            entry = Entry(description=request.form['description'], template=request.form['template'], user=user)
            db.session.add(entry)
            db.session.commit()
            flash("entry added")
        else:
            flash("enter a description and template")
        return redirect(url_for('routes.show_entries'))
    else:
        return render_template('add_entries.html')

@routes.route('/users', methods=['GET'])
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@routes.route('/view_profile', methods=['GET', 'POST'])
def view_profile():
    # this will delete entries if delete button is pressed
    if request.method == "POST":
        print("success");
        entry_id = int(request.form["entry_id"])
        Entry.query.filter(Entry.id == entry_id).delete()
        db.session.commit()
        return json.dumps({'status':'OK'});
    else:
        # otherwise, it will display all their entries
        username = session['user']
        entries = User.query.filter(User.name == username).one().submissions
        entries = enumerate(entries, 1)
        return render_template('user_profile.html', entries=entries)
