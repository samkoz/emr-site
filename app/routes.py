from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session, json
from sqlalchemy import desc
from .db import db, Entry, User
from .forms import LogginForm, SignUpForm

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
    username = None
    form = LogginForm()
    if form.validate_on_submit():
        current_users = [user[0] for user in db.session.query(User.name).all()]
        username = form.name.data
        form.name.data = ""
        if username in current_users:
            session['logged_in'] = True
            user = User.query.filter(User.name == username).one()
            session['user'] = username
            flash("sign in successful")
            return redirect(url_for("routes.view_profile", username=username))
        else:
            flash("you need to sign up")
            # this prevents resubmitting the post request
            return redirect(url_for("routes.show_log_in"))
    return render_template('log_in.html', form=form)

@routes.route('/sign_up', methods=['GET', 'POST'])
def show_sign_up():
    username = None
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.name.data
        institution = form.institution.data
        current_users = [user[0] for user in db.session.query(User.name).all()]

        if username not in current_users:
            new_user = User(name=username, institution=institution)
            db.session.add(new_user)
            db.session.commit()
            flash("sign up successful")
            session["logged_in"] = True
            session["user"] = new_user.name
            return redirect(url_for("routes.view_profile", username=username))

        else:
            flash("username already in database - choose something else")
            return redirect(url_for('routes.show_sign_up'))
    else:
        return render_template('sign_up.html', form=form)

@routes.route('/show_entries', methods=['GET', 'POST'])
# will need to include order here somehow...
def show_entries():
    if request.method == "POST":
        entry_id = int(request.form["entry_id"])
        print(entry_id)
        entry = Entry.query.filter(Entry.id == entry_id).one()
        user = User.query.filter(User.name == session['user']).one()
        print(entry)
        print(user)
        message = ""
        if entry in user.submissions:
            message = "You cannot save an entry you have submitted"
            status = "Error"
        elif entry in user.saved_entries:
            message = "You have already saved this entry"
            status = "Error"
        else:
            if entry.num_user_saves == 0:
                entry.user_saves = [user]
            else:
                entry.user_saves.append(user)

            db.session.add_all([user, entry])
            db.session.commit()
            status = 'OK'

        return json.dumps({'status': status, "data" : [message, entry.num_user_saves()]});

    else:
        entries = Entry.query.order_by(desc(Entry.id)).all()
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

@routes.route('/view_profile/<username>', methods=['GET', 'POST'])
def view_profile(username):
    # this will delete entries if delete button is pressed
    if request.method == "POST":
        print("success");
        entry_id = int(request.form['entry_id'])
        entry_type = request.form['entry_type']
        if entry_type == 'submission':
            Entry.query.filter(Entry.id == entry_id).delete()
            # will need to remove it from all other users saves...?
            # how to handle updates / edits?
            db.session.commit()
        elif entry_type == 'saved':
            user = User.query.filter(User.name == session['user']).one()
            print(user)
            saved_entries = user.saved_entries
            saved_entries = [entry for entry in saved_entries if entry.id != entry_id]
            user.saved_entries = saved_entries
            db.session.add(user)
            db.session.commit()
        else:
            raise KeyError
        return json.dumps({'status':'OK'});
    else:
        # otherwise, it will display all their submitted and saved entries
        username = session['user']
        user = User.query.filter(User.name == username).one()
        user_entries = user.submissions
        saved_entries = user.saved_entries
        user_entries = enumerate(user_entries, 1)
        saved_entries = enumerate(saved_entries, 1)
        return render_template('user_profile.html', user_entries=user_entries, saved_entries=saved_entries)
