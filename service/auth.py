import datetime
import calendar

import jwt
from flask import request
from flask_restx import abort

from constants import JWT_SECRET, JWT_ALGORITHM
from exceptions import InvalidToken, WrongPassword
from service.user import UserService


# класс для реализации бизнес логики
class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, authorization_data, is_refresh=False) -> dict:
        """Создание доступа и обновление токенов JWT"""

        # получить данные пользователя
        email_data = authorization_data.get('email')
        password_data = authorization_data.get('password')
        user = self.user_service.get_by_email(email_data)

        # сравнение паролей
        if not is_refresh:
            password_is_correct = self.user_service.compare_passwords(user.password, password_data)
            if not password_is_correct:
                raise WrongPassword

        # данные для генерации токена
        data = {
            'email': user.email
        }

        # генерируем токен доступа (minutes=30)
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp']: int = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # генерируем токен обновления (days=130)
        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp']: int = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def get_email_from_token(self, token: str) -> str:
        """Возвращает данные (email) пользователя из токена"""
        try:

            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            email = data.get('email')

            return email

        except Exception:
            raise InvalidToken

    def approve_refresh_token(self, refresh_token: str) -> dict:
        """Подтверждение токена обновления и создание новой пары токенов"""
        # генерация данных для токена и создание новых токенов
        authorization_data = {
            'email': self.get_email_from_token(refresh_token),
            'password': None
        }
        new_tokens = self.generate_tokens(authorization_data, is_refresh=True)

        return new_tokens

    @staticmethod
    def auth_required(func):
        """Проверяем правильность переданного токена"""

        def wrapper(*args, **kwargs):
            # проверяем были ли переданы учетные данные авторизации и получаем токен
            if 'Authorization' not in request.headers:
                abort(401, 'Данные авторизации не переданы')

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]

            # декодирование токена
            try:
                jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                abort(401, f'JWT decode Exception {e}')

            return func(*args, **kwargs)

        return wrapper
