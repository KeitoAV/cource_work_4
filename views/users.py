from flask import request
from flask_restx import Resource, Namespace, fields, abort

from dao.model.user import UserSchema
from exceptions import WrongPassword, MethodNotAvailable
from implemented import auth_service, user_service
from views.genres import genre_model

user_ns = Namespace('user', description="Views for users")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# api model
user_model = user_ns.model('User', {
    'id': fields.Integer(required=False),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(),
    'surname': fields.String(),
    'favourite_genre': fields.Integer(),
    'genre': fields.Nested(required=True, model=genre_model),
})


@user_ns.route('/')
@user_ns.response(200, 'Success', user_model)
@user_ns.response(404, 'Not Found')
class UserView(Resource):
    @user_ns.doc(description='Get user info')
    @auth_service.auth_required
    def get(self):
        """Получить информацию о пользователе (его профиль)"""

        # получить токен
        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        # получить данные
        user = user_service.get_by_email(email)
        user_info = user_schema.dump(user)
        return user_info, 200

    @user_ns.doc(description='Update user info')
    @auth_service.auth_required
    def patch(self):
        """Изменить информацию пользователя (имя, фамилия, любимый жанр)"""
        try:
            # получить токен
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)

            # получить и обновить данные
            updated_d = user_schema.dump(request.json)
            user_service.update_data(updated_d, email)
            return 'Данные пользователя успешно обновлены', 200
        except MethodNotAvailable:
            abort(405, messege='Вам не разрешено изменять переданные данные')


@user_ns.route('/password/')
@user_ns.response(200, 'Success', user_model)
@user_ns.response(404, 'Not Found')
class PasswordView(Resource):
    @user_ns.doc(description='Update user password')
    @auth_service.auth_required
    def put(self):
        """Обновить пароль пользователя"""
        try:
            # получить токен
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)

            # получить и обновить данные
            passwords = request.json
            user_service.update_password(passwords, email)
            return "Пароль успешно обновлен", 200

        except WrongPassword:
            abort(401, messege='Неверный пароль')

