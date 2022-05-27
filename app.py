from flask import Flask, jsonify

from utils import search_title, search_by_years, sort_by_rating, search_by_genre
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/movie/<title>')
def movie_title(title):
    return jsonify(search_title(title))


@app.route('/movie/<int:year1>/to/<int:year2>')
def movie_by_year(year1, year2):
    return jsonify(search_by_years(year1, year2))


@app.route('/rating/children')
def movie_from_children():
    return jsonify(sort_by_rating('children'))


@app.route('/rating/family')
def movie_from_family():
    return jsonify(sort_by_rating('family'))


@app.route('/rating/adult')
def movie_from_adult():
    return jsonify(sort_by_rating('adult'))


@app.route('/genre/<genre>')
def movie_by_genre(genre):
    return jsonify(search_by_genre(genre))


if __name__ == '__main__':
    app.run(debug=True)
