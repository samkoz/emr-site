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


## These aren't working...
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
