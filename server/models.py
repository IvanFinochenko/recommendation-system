from app import db, bcrypt
from flask_login import UserMixin

class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50))

    def __init__(self, genre_id, genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name

    def __repr__(self):
        return '<id {}>'.format(self.genre_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = db.session.query(db.func.max(User.user_id))[0][0]
        if not user_id:
            user_id = 0
        self.user_id = user_id + 1

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<id {}>'.format(self.user_id)

class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    country = db.Column(db.String(50))
    director = db.Column(db.String(50))
    rating = db.Column(db.Float)
    runtime = db.Column(db.Integer)
    count_reviews = db.Column(db.Integer)
    percent_good_reviews = db.Column(db.Float)
    critics_rating = db.Column(db.Integer)
    critics_rating_russian = db.Column(db.Integer)
    budget = db.Column(db.BigInteger)
    box_office = db.Column(db.BigInteger)
    age = db.Column(db.Integer)
    image = db.Column(db.Integer)
    poster = db.Column(db.String(255))

class MoviesGenre(db.Model):
    __tablename__ = 'movies_genre'

    movie_id = db.Column(db.Integer, primary_key=True)
    genre_id =  db.Column(db.Integer, primary_key=True)

class Rating(db.Model):
    __tablename__ = 'ratings'

    user_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer)

    def __init__(self, user_id, movie_id, vote):
        self.user_id = user_id
        self.movie_id = movie_id
        self.vote = vote


class UserMovie(db.Model):
    __tablename__ = 'user_movies'

    user_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    prev_recommendation = db.Column(db.Integer)

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id
        self.type = 'watchlist'
        self.prev_recommendation = 0