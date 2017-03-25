from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from .factory import create_app
from .db import db

# from flask import render_template

app = create_app(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

# run flask db init to initialize
migrate = Migrate(app, db)
