from .fixtures import db, app, session, client
from flask import url_for
from app.db import User, Entry

# The problem was that I wasn't passing db into this fuction
# Therefore, the fixtures.db fixture function (which includes create_all() ...)
# wasn't being executed. Thus, the tables didn't exist.
# So remember, if you want to test anything that has to do with the database,
# remember to pass the db fixture into the test definition!
def test_route(app, db, session, client):
    res = client.get('/')
    assert res.status_code == 200

def test_relationship(db, session):
    user = Users(name="Sam", institution="UofM")
    entry = Entries(description="Smarty", template="template", user=user)

    print(db.session.execute('show tables').fetchall())
    print(db.session.execute('select * from entries').fetchall())
    print(db.session.execute('select * from test.entries').fetchall())

    session.add_all([user, entry])
    session.commit()

    assert entry in user.submissions
    assert entry.user is user
