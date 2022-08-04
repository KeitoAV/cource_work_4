from flask import request
from flask_restx import Resource, Namespace, abort, fields

from dao.model.director import DirectorSchema
from exceptions import PostNotFound
from implemented import director_service

director_ns = Namespace('directors', description='Views for directors')
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

# api model
director_model = director_ns.model('Director', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True)
})


@director_ns.route('/')
class DirectorsView(Resource):
    @director_ns.doc(description='Get directors',
                     params={'page': 'Page number',
                             })
    @director_ns.response(200, 'Success', director_model)
    @director_ns.response(404, 'Not found')
    def get(self):
        try:
            page = request.args.get('page')

            directors = director_service.get_all(page, status=False)

            return directors_schema.dump(directors), 200
        except PostNotFound:
            abort(404, messege=f'Страница не найдена')


@director_ns.route('/<int:did>/')
class DirectorView(Resource):
    @director_ns.doc(description='Get director by ID')
    @director_ns.response(200, 'Success')
    @director_ns.response(404, 'Not found')
    def get(self, did):
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except PostNotFound:
            abort(404, messege=f'Режиссёр {did} не найден')
