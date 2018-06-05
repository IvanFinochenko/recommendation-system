from app import app, db, login
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, abort
from flask_login import login_user, logout_user, current_user
from models import *
import subprocess
import math


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api/login', methods=['POST'])
def login():
    incoming = request.get_json()
    user = User.query.filter_by(username=incoming['username']).first()
    if user and user.check_password(incoming['password']):
        try:
            login_user(user=user, remember=True)
        except:
            print("login error")
        return jsonify(id=user.user_id, username=user.username)
    else:
        return jsonify(), 401


@app.route('/api/signup', methods=['POST'])
def signup():
    incoming = request.get_json()
    if User.query.filter_by(username=incoming['username']).first():
        return jsonify(), 409
    user = User(username=incoming['username'], password=incoming['password'])
    db.session.add(user)

    try:
        db.session.commit()
        login_user(user=user, remember=True)
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    return jsonify(id=user.user_id, username=user.username)


@app.route('/api/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify()


@app.route('/api/movie/<movie_id>', methods=['GET'])
def movie(movie_id):
    movie = Movie.query.get(movie_id)
    genres = MoviesGenre.query.filter_by(movie_id=movie_id).all()
    genres_list = []
    image = None
    if movie.image == 1:
        image = 'Цветное'
    if movie.image == 0:
        image = 'Чёрно-белое'
    for genre in genres:
        genres_list.append(Genre.query.get(genre.genre_id).genre_name)
    votes_user = Rating.query.filter_by(user_id=current_user.get_id()).all()
    user_vote = None
    for vote in votes_user:
        if movie.movie_id == vote.movie_id:
            user_vote = vote.vote
    return jsonify(
        title=movie.title,
        year=movie.year,
        country=movie.country,
        director=movie.director,
        rating=movie.rating,
        runtime=movie.runtime,
        count_reviews=movie.count_reviews,
        percent_good_reviews=movie.percent_good_reviews,
        critics_rating=movie.critics_rating,
        critics_rating_russian=movie.critics_rating_russian,
        budget=movie.budget,
        box_office=movie.box_office,
        age=movie.age,
        image=image,
        genres=', '.join(genres_list),
        poster_url=movie.poster,
        vote=user_vote)


@app.route('/api/movies/<int:page>', methods=['GET'])
def movies(page):
    genre_id = int(request.args.get('genre_id', -1))
    type_search = int(request.args.get('type_search', 1))
    text_search = request.args.get('text_search', "")
    per_page = 10
    movies = None
    if genre_id == -1:
        movies = Movie.query.order_by(Movie.movie_id.desc())
    if not genre_id == -1:
        movies_genres = MoviesGenre.query.filter_by(genre_id=genre_id).all()
        movies_id_list = map(lambda x: x.movie_id, movies_genres)
        movies = Movie.query \
            .filter(Movie.movie_id.in_(movies_id_list)) \
            .order_by(Movie.movie_id.desc())
    if not text_search == "":
        if type_search == 1:
            movies = movies.filter(Movie.title.contains(text_search))
        if type_search == 2:
            movies = movies.filter(Movie.director.contains(text_search))
        if type_search == 3:
            movies = movies.filter(Movie.country.contains(text_search))
    count_page = (movies.count() / 10)
    movies = movies.paginate(page, per_page, error_out=False).items
    movies_list = []
    votes_user = Rating.query.filter_by(user_id=current_user.get_id()).all()
    for movie in movies:
        user_vote = None
        isWatchlist = False
        for vote in votes_user:
            if movie.movie_id == vote.movie_id:
                user_vote = vote.vote
        if current_user.is_authenticated:
            if UserMovie.query.filter_by(user_id=current_user.get_id()).filter_by(movie_id=movie.movie_id).first():
                isWatchlist = True
        movies_list.append({
            'id': movie.movie_id,
            'title': movie.title,
            'year': movie.year,
            'country': movie.country,
            'rating': movie.rating,
            'poster_url': movie.poster,
            'vote': user_vote,
            'isWatchlist': isWatchlist
        })
    return jsonify(movies=movies_list, count_page=count_page)


@app.route('/api/rating', methods=['POST'])
def rating():
    print(current_user.get_id())
    user_id = current_user.user_id
    incoming = request.get_json()
    movie_id = incoming['movie_id']
    vote = incoming['rating']
    rating = Rating(user_id=user_id, movie_id=movie_id, vote=vote)
    db.session.add(rating)
    user_movie = UserMovie.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
    if user_movie:
        db.session.delete(user_movie)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409
    count_ratings = Rating.query.filter_by(user_id=user_id).count()
    if count_ratings == 10:
        subprocess.call(['./recommendation-engine/recommendations/start.sh', user_id])
        User.query.filter_by(user_id=user_id).update(dict(prev_recommendation=10))
    prev_recommendation = User.query.filter_by(user_id=user_id).first().prev_recommendation
    if count_ratings - prev_recommendation == 50:
        subprocess.call(['./recommendation-engine/recommendations/start.sh', user_id])
        User.query.filter_by(user_id=user_id).update(dict(prev_recommendation=(prev_recommendation + 50)))

    return jsonify()


@app.route('/api/genres', methods=['GET'])
def genres():
    genres = Genre.query.all()
    genres_list = []
    for genre in genres:
        genres_list.append({'value': genre.genre_id, 'label': genre.genre_name})
    return jsonify(genres=genres_list)


@app.route('/api/recommendations', methods=['GET'])
def recommendation():
    if Rating.query.filter_by(user_id=current_user.get_id()).count() < 10:
        return jsonify(), 409
    movies = Movie.query.join(UserMovie, Movie.movie_id == UserMovie.movie_id) \
        .filter_by(user_id=current_user.get_id()).filter_by(type='recommendation')
    print(movies)
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie.movie_id,
            'title': movie.title,
            'year': movie.year,
            'country': movie.country,
            'rating': movie.rating,
            'poster_url': movie.poster
        })
    return jsonify(movies=movies_list)


@app.route('/api/watchlist', methods=['GET', 'POST', 'DELETE'])
def watchlist():
    if request.method == 'POST':
        del_movie = UserMovie.query.filter_by(user_id=current_user.get_id()).filter_by(movie_id=request.get_json()['movie_id']).first()
        if del_movie:
            db.session.delete(del_movie)
        user_movie = UserMovie(user_id=current_user.get_id(), movie_id=request.get_json()['movie_id'])
        db.session.add(user_movie)
        try:
            db.session.commit()
        except IntegrityError:
            return jsonify(), 409
        return jsonify(id=user_movie.movie_id)

    if request.method == 'GET':
        page = int(request.args.get('page', 0))
        watchlist_query = UserMovie.query.filter_by(user_id=current_user.get_id()).filter_by(type='watchlist')
        watchlist = watchlist_query.order_by(UserMovie.movie_id.desc()).paginate(page, 10, error_out=False).items
        watch_list = []
        for movie_id in watchlist:
            movie = Movie.query.get(movie_id.movie_id)
            watch_list.append({
            'id': movie.movie_id,
            'title': movie.title,
            'year': movie.year,
            'country': movie.country,
            'rating': movie.rating,
            'poster_url': movie.poster,
            'isWatchlist': True
        })
        count_page = watchlist_query.count() / 10
        return jsonify(movies=watch_list, count_page=count_page)

    if request.method == 'DELETE':
        user_movie = UserMovie.query.filter_by(user_id=current_user.get_id()).filter_by(movie_id=request.get_json()['movie_id']).first()
        if user_movie:
            db.session.delete(user_movie)
            db.session.commit()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8082')
    response.headers.add('Access-Control-Allow-Headers', "Access-Control-Allow-Origin, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Header")
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
