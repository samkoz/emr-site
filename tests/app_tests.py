from tests.fixtures import db, app, session, client
from flask import url_for
from app.db import User, Entry

# The problem was that I wasn't passing db into this fuction
# Therefore, the fixtures.db fixture function (which includes create_all() ...)
# wasn't being executed. Thus, the tables didn't exist.
# So remember, if you want to test anything that has to do with the database,
# remember to pass the db fixture into the test definition!

# run with this: py.test tests/app_tests.py

def test_route(app, db, session, client):
    res = client.get('/')
    assert res.status_code == 200
    res = client.get('/log_in')
    assert res.status_code == 200
    res = client.get('/sign_up')
    assert res.status_code == 200
    res = client.get('/show_entries')
    assert res.status_code == 200
    res = client.get('/add')
    assert res.status_code == 405
    res = client.get('/delete')
    assert res.status_code == 405

def test_relationship(db, session):
    user = User(name="Sam", institution="UofM")
    entry = Entry(description="Smarty", template="template", user=user)

    print(db.session.execute('show tables').fetchall())
    print(db.session.execute('select * from entries').fetchall())
    print(db.session.execute('select * from test.entries').fetchall())

    session.add_all([user, entry])
    session.commit()

    assert entry in user.submissions
    assert entry.user is user

def test_current_user(db, session):
    user = User(name="sam", institution="UofM")
    entry = Entry(description="desc", template="temp", user=user)
    session.add_all([user, entry])
    session.commit()

    current_users = [user[0] for user in db.session.query(User.name).all()]
    assert user.name in current_users
