from flask import request
from flask_restx import Resource
from marshmallow import Schema, fields
from config import api, app
from create_data import *

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    director_name = fields.Str()
    genre_name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self, page=1):
        movies_query = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies = movies_query.paginate(page, per_page=5)

        return movies_schema.dump(movies.items), 200

    def post(self):
        req_json = request.json
        new_movies = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movies)
        return "", 201


@movies_ns.route("/<int:uid>")
class MoviesView(Resource):
    def get(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return "", 404
        return movie_schema.dump(movie), 200

    def put(self, uid):
        updated_rows = db.session.query(Movie).filter(Movie.id == uid).update(request.json)
        if updated_rows != 1:
            return "", 400
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        delete_rows = db.session.query(Movie).get(uid)
        if not delete_rows:
            return "", 400
        db.session.delete(delete_rows)
        db.session.commit()
        return "", 204


@directors_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director)
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_directors = Director(**req_json)
        with db.session.begin():
            db.session.add(new_directors)
        return "", 201


@directors_ns.route("/<int:uid>")
class DirectorsView(Resource):
    def get(self, uid: int):
        directors = db.session.query(Director).get(uid)
        if not directors:
            return "", 404
        return director_schema.dump(directors), 200

    def put(self, uid: int):
        updated_rows = db.session.query(Director).filter(Director.id == uid).update(request.json)
        if updated_rows != 1:
            return "", 400
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        delete_rows = db.session.query(Director).get(uid)
        if not delete_rows:
            return "", 400
        db.session.delete(delete_rows)
        db.session.commit()
        return "", 204


@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre)
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genres_ns.route("/<int:uid>")
class GenresView(Resource):
    def get(self, uid: int):
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return "", 404
        return genre_schema.dump(genre), 200

    def put(self, uid):
        updated_rows = db.session.query(Genre).filter(Genre.id == uid).update(request.json)
        if updated_rows != 1:
            return "", 400
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        delete_rows = db.session.query(Genre).get(uid)
        if not delete_rows:
            return "", 400
        db.session.delete(delete_rows)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
