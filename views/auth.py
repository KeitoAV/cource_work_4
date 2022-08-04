from flask import request
from flask_restx import Resource, Namespace, fields, abort

from dao.model.user import UserSchema
from exceptions import WrongPassword, InvalidToken
from implemented import user_service, auth_service

auth_ns = Namespace('auth', description='Views for auth')
user_schema = UserSchema()

# api model
auth_model = auth_ns.model('Registration', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

tokens_model = auth_ns.model('Tokens', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})


@auth_ns.route('/register/')
class AuthView(Resource):
    @auth_ns.doc(description='User registration', body=auth_model)
    @auth_ns.response(201, 'Success')
    @auth_ns.response(400, 'Not found')
    def post(self):
        # получить учетные данные
        data_auth = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in data_auth.values():
            abort(400, messege='Не удалось зарегистрироваться')

        # регистрация пользователя

        data = user_schema.load(data_auth)
        user = user_service.create(data)
        return "Пользователь успешно создан", 201, {"location": f"/auth/register/{user.id}"}


@auth_ns.route('/login/')
class AuthView(Resource):
    @auth_ns.doc(description='User authorization', body=auth_model)
    @auth_ns.response(201, 'Tokens created', tokens_model)
    @auth_ns.response(401, 'Wrong password')
    def post(self):
        # получить и проверить переданные учетные данные
        data_auth = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }

        # генерация токенов
        try:
            tokens = auth_service.generate_tokens(data_auth)
            return tokens, 201

        except WrongPassword:
            abort(401, messege='Неверный пароль')

    @auth_ns.doc(description='Update token by user')
    @auth_ns.response(201, 'Tokens updated', tokens_model)
    @auth_ns.response(401, 'Invalid refresh token')
    def put(self):
        try:
            # проверить достоверность данных
            refresh_token = request.json.get('refresh_token')
            if not refresh_token:
                abort(400, 'Переданы неверные данные')

            # обновление hash-пароля пользователя
            tokens = auth_service.approve_refresh_token(refresh_token)
            return tokens, 201

        except InvalidToken:
            abort(401, 'Передан неверный токен')
