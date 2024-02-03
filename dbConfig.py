from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Will be connected to Flask app in Main
db = SQLAlchemy()

#Define Tables Below:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
