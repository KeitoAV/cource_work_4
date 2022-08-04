from flask import request
from flask_restx import Resource, Namespace, abort, fields

from dao.model.movie import MovieSchema
from exceptions import PostNotFound
from implemented import movie_service
from views.directors import director_model
from views.genres import genre_model

movie_ns = Namespace('movies', description='Views for movies')
movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

# api model
movie_model = movie_ns.model('Movie', {
    'id': fields.Integer(required=False),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'trailer': fields.String(required=True),
    'year': fields.Integer(required=True),
    'rating': fields.Float(required=True),
    'genre': fields.Nested(required=True, model=genre_model),
    'director': fields.Nested(required=True, model=director_model)
})


@movie_ns.route('/')
@movie_ns.response(200, 'Success', movie_model)
@movie_ns.response(404, 'Not found')
class MoviesView(Resource):
    @movie_ns.doc(description='Get movies',
                  params={'page': 'Page number',
                          'status': 'New'})
    def get(self):
        try:
            page = request.args.get('page')
            status = request.args.get('status')
            movies = movie_service.get_all(page, status)

            return movies_schema.dump(movies), 200
        except PostNotFound:
            abort(404, messege='Страница не найдена')


@movie_ns.route('/<int:mid>/')
@movie_ns.response(200, 'Success')
@movie_ns.response(404, 'Not found')
class MovieView(Resource):
    @movie_ns.doc(description='Get movie by ID')
    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except PostNotFound:
            abort(404, messege=f'Фильм {mid} не найден')


