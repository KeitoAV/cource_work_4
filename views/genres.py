from flask import request
from flask_restx import Resource, Namespace, abort, fields

from dao.model.genre import GenreSchema
from exceptions import PostNotFound
from implemented import genre_service

genre_ns = Namespace('genres', description='Views for genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

# api model
genre_model = genre_ns.model('Genre', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True)
})


@genre_ns.route('/')
class GenresView(Resource):
    @genre_ns.doc(description='Get genres',
                  params={'page': 'Page number',
                          })
    @genre_ns.response(200, 'Success', genre_model)
    @genre_ns.response(404, 'Not found')
    def get(self):
        try:
            page = request.args.get('page')

            genres = genre_service.get_all(page, status=False)

            return genres_schema.dump(genres), 200
        except PostNotFound:
            abort(404, messege=f'Страница не найдена')


@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    @genre_ns.doc(description='Get genre by ID')
    @genre_ns.response(200, 'Success')
    @genre_ns.response(404, 'Not found')
    def get(self, gid):
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except PostNotFound:
            abort(404, messege=f'Жанр {gid} не найден')
