from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean)
    notes = db.relationship('Note')
    preferences = db.Column(db.String(150000))  # list with 19331 members
    vector = db.Column(db.String(1500))  # list with 43 members

class Rating(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    item_row = db.Column(db.Integer)   # row index in dataframe items
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    imageLink = db.Column(db.String(250))
