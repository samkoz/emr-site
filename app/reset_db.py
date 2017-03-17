from .app import app
from .db import db

def reset_db():
    with app.app_context():
        print("DB reset!")
        db.drop_all()
        db.create_all()

# run with: python -m reset_db FROM parent module or import it and run it
if __name__ == '__main__':
    reset_db()
