from fixtures import app, db, session



def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
