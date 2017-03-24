from .factory import create_app
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from flask import render_template

app = create_app(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
