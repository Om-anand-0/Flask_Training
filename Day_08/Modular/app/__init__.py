from flask import Flask
from .database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

from . import routes

with app.context():
    db.create_all()
