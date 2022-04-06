from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Movie(db.Model):
    __tablename__ = 'movie'
    imdb_id = db.Column(db.String(100), primary_key=True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(1000))
    plot = db.Column(db.String(1000))
    img_url = db.Column(db.String(1000))
    reviews = db.relationship('Review', backref='movie', lazy=True)

class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = db.PrimaryKeyConstraint('movie_id', 'user_id'),
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.imdb_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_content = db.Column(db.String(1000))
    stars = db.Column(db.Integer)
    