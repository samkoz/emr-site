import os
from flask import Flask, g
from flask import render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from raven.contrib.flask import Sentry
from flask_script import Manager
from .db import db, User
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
moment = Moment()
bootstrap = Bootstrap()
sentry = Sentry(dsn='https://1fa9120946234be4aefd3f68321f4061:a13041d75a79469681dfb52bad961fe5@sentry.io/151943')
manager = Manager()
migrate = Migrate()

def create_app(name):
    app = Flask(name)
    app.register_blueprint(routes)
    print('RUNNING IN "{}"'.format(get_env()))
    print("Env:", get_env())
    app.config.from_object(get_config())
    app.config.from_object(get_secrets())
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    sentry.init_app(app)
    migrate.init_app(app, db)

    # These aren't working...
    @routes.app_errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # will need to do some imports here to get sentry to work (g)
    @routes.app_errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html',
            event_id=g.sentry_event_id,
            public_dsn=sentry.client.get_public_dsn('https')
        )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app
