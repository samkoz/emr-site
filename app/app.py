from .factory import create_app
from .db import db
# from flask import render_template

app = create_app(__name__)
