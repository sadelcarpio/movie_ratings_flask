from flask import Blueprint, jsonify, request
from flask_login import login_required
from bs4 import BeautifulSoup
from .models import Movie
import os, requests
from . import db

IMDB_API = 'https://imdb-api.com/en/API/SearchMovie/{}/'.format(os.environ.get('API_KEY'))
IMDB_MOVIE_URL = 'http://imdb.com/title/'

movies = Blueprint('movies', __name__)

@movies.route('/all', methods=['GET'])
def movies_get():
    movies = Movie.query.all()
    result = []
    for movie in movies:
        result.append({
            'imdb_id': movie.imdb_id,
            'year': movie.year,
            'title': movie.title,
            'plot': movie.plot,
            'img_url': movie.img_url
        })
    return jsonify(result)

@movies.route('/search', methods=['POST'])
def movie_search():
    movie = request.get_json(force=True)['searchMovie']
    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    response = requests.get(IMDB_API + movie, headers=headers)
    return response.json(), 200

@movies.route('/create', methods=['POST'])
def movie_create():
    movie_noplot = request.get_json(force=True)
    imdb_id = movie_noplot['imdb_id']
    cookies = {"lc-main": "es_ES"}
    s = requests.session()
    r = s.get(url=IMDB_MOVIE_URL + imdb_id + '/', cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    plot = soup.find_all("span", {"class": "sc-16ede01-2 gXUyNh"})[0].text
    db.session.add(Movie(**movie_noplot, plot=plot))
    db.session.commit()
    return jsonify(['Película añadida con éxito!']), 201