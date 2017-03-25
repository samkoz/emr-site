import os
from flask import Flask
from flask import render_template
from flask_login import LoginManager
from .db import db
from . import config
from . import secrets
from .routes import routes


def get_env():
    try:
        env = os.environ["ENV"]
        return env
    except KeyError:
        print("Set your Environment Variable\n")
        raise

def get_config():
    env = get_env()
    try:
        return getattr(config, env.capitalize())
    except AttributeError:
         print("Please specify a valid config in the Environment variable\ne.g. $env:ENV='prod'\n\n")
         raise

def get_secrets():
    env = get_env()
    try:
        return getattr(secrets, env.capitalize())
    except AttributeError:
         print("Please specify a valid config in the Environment variable\ne.g. $env:ENV='prod'\n\n")
         raise

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(name):
    app = Flask(name)
    app.register_blueprint(routes)
    print('RUNNING IN "{}"'.format(get_env()))
    print("Env:", get_env())
    app.config.from_object(get_config())
    app.config.from_object(get_secrets())
    db.init_app(app)
    login_manager.init_app(app)

    # These aren't working...
    @routes.app_errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @routes.app_errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
