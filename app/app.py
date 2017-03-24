from .factory import create_app
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = create_app(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)
