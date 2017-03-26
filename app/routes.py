from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session, json
from flask_login import login_user, logout_user, current_user
from sqlalchemy import desc
from .db import db, Entry, User
from .forms import LogginForm, SignUpForm, AddEntryForm, SearchForm

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def show_landing():
    return render_template('landing.html')

@routes.route('/test_entries')
def gen_test_entries():
    Entry.generate_fake()
    return redirect(url_for('routes.show_entries'))


@routes.route('/log_out')
def log_out():
    logout_user()
    flash("you were logged out")
    return redirect(url_for('routes.show_landing'))

@routes.route('/log_in', methods=['GET', 'POST'])
def show_log_in():
    username = None
    form = LogginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        form.name.data = ""
        form.password.data = ""
        user = User.query.filter(User.name == username.lower()).first()
        if user is not None and user.verify_password(password):
            session['user'] = username
            flash("sign in successful")
            login_user(user, form.remember_me.data)
            return redirect(url_for("routes.view_profile", username=username))
        else:
            flash("incorrect username or password. sign up if you have not signed up!")
            return redirect(url_for("routes.show_log_in"))
    return render_template('log_in.html', form=form)

@routes.route('/sign_up', methods=['GET', 'POST'])
def show_sign_up():
    username = None
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.name.data
        institution = form.institution.data
        password = form.password.data
        current_user = User.query.filter(User.name == username.lower()).first()
        if not current_user:
            new_user = User(name=username, institution=institution, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("sign up successful")
            login_user(new_user)
            return redirect(url_for("routes.view_profile", username=username))
        else:
            flash("username already in database - choose something else")
            return redirect(url_for('routes.show_sign_up'))
    else:
        return render_template('sign_up.html', form=form)

@routes.route('/show_entries', methods=['GET', 'POST'])
def show_entries():
    form = SearchForm()
    entry_list = []
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_order = form.search_order.data
        specialty = form.specialty.data
        note_type = form.note_type.data
        note_part = form.note_part.data
        return redirect(url_for('routes.show_entries', q=search_query, search_order=search_order,
            specialty=specialty, note_type=note_type, note_part=note_part))

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
            entry.num_user_saves += 1

            db.session.add_all([user, entry])
            db.session.commit()
            status = 'OK'

        return json.dumps({'status': status, "data" : [message, entry.num_user_saves]});

    else:
        q = request.args.get('q')
        search_order = request.args.get('search_order')
        specialty = request.args.getlist('specialty')
        note_part = request.args.getlist('note_part')
        note_type = request.args.getlist('note_type')
        page = request.args.get('page', 1, type=int)

        if q:
            entries = Entry.query.filter((Entry.description.contains(q)) \
                | (Entry.template.contains(q)))
            if search_order == "submission_time":
                pagination = entries.order_by(desc(Entry.time_created)).paginate(page, per_page=30, error_out=False)
            elif search_order == 'saves':
                pagination = entries.order_by(desc(Entry.num_user_saves)).paginate(page, per_page=30, error_out=False)
        else:
            pagination = Entry.query.order_by(desc(Entry.time_created)).paginate(page, per_page=30, error_out=True)
        endpoint = '.show_entries'
        entries = pagination.items
        entries = entries

        # preserve form values
        form.search_query.data = q
        if search_order:
            form.search_order.data = search_order
        else:
            form.search_order.data = 'submission_time'
        form.specialty.data = specialty
        form.note_part.data = note_part
        form.note_type.data = note_type

        return render_template('entries.html', entries=entries, pagination=pagination, form=form, q=q, endpoint=endpoint)

@routes.route('/add', methods=['GET', 'POST'])
def add_entry():
    form = AddEntryForm()
    if form.validate_on_submit():
        description = form.description.data
        template = form.template.data
        # form.description.data = ''
        # form.template.data = ''
        user = User.query.filter(User.name == session['user']).one()
        entry = Entry(description=description, template=template, user=user)
        db.session.add(entry)
        db.session.commit()
        flash("entry added")
        return redirect(url_for('routes.add_entry'))
    else:
        return render_template('add_entries.html', form=form)

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
        entry = Entry.query.filter(Entry.id == entry_id)
        if entry_type == 'submission':
            entry.delete()
            db.session.commit()
        elif entry_type == 'saved':
            user = User.query.filter(User.name == session['user']).one()
            entry = entry.one()
            print(user)
            saved_entries = user.saved_entries
            saved_entries = [entry for entry in saved_entries if entry.id != entry_id]
            user.saved_entries = saved_entries
            entry.num_user_saves -= 1
            db.session.add_all([user, entry])
            db.session.commit()
        else:
            raise KeyError
        return json.dumps({'status':'OK'});
    else:
        # otherwise, it will display all their submitted and saved entries
        if current_user.is_anonymous or current_user.name != username:
            current = False
            user = User.query.filter(User.name == username).one()
            username = user.name
            if username[-1] == 's':
                username += "' profile"
            else:
                username += "'s profile"
        else:
            user = current_user
            current = True
            username = 'Your profile'
        user_entries = user.submissions
        saved_entries = user.saved_entries
        user_entries = user_entries
        saved_entries = saved_entries
        return render_template('user_profile.html',
            user_entries=user_entries,
            saved_entries=saved_entries,
            username=username,
            current=current)
