from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from .factory import create_app
from .db import db, User, Entry

app = create(app)
manager = Manager(app)

manager.init_app(app)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Entry=Entry)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if name == "__main__":
    manager.run()
