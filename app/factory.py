import os
from flask import Flask
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

def create_app(name):
    app = Flask(name)
    app.register_blueprint(routes)
    print('RUNNING IN "{}"'.format(get_env()))
    print("Env:", get_env())
    app.config.from_object(get_config())
    app.config.from_object(get_secrets())
    db.init_app(app)
    return app
