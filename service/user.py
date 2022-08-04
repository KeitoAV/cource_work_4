import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.user import User
from dao.user import UserDAO
from exceptions import PostNotFound, MethodNotAvailable, WrongPassword


# класс для реализации бизнес логики
class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_email(self, email: str):
        """Получить пользователя по email"""
        user = self.dao.get_by_email(email)

        return user

    def get_all(self, page, status) -> list[User]:
        """Получить всех пользователей """
        users = self.dao.get_all(page, status)

        return users

    def create(self, user_d: dict):
        """Добавить нового пользователя"""
        # hash-пароль
        user_d['password'] = self.generate_password(user_d.get('password'))
        # обновление в базе
        user_data = self.dao.create(user_d)
        return user_data

    def update_data(self, data: dict, email: str) -> None:
        """Обновление данных пользователя"""
        # получить данные пользователя
        self.get_by_email(email)
        # проверить данные
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update_by_email(data, email)
        else:
            raise MethodNotAvailable

    def update_password(self, data: dict, email: str):
        """Обновление пароля """
        # проверить данные
        user = self.get_by_email(email)
        current_password = data.get('old_password')
        new_password = data.get('new_password')

        if None in [current_password, new_password]:
            raise MethodNotAvailable

        if not self.compare_passwords(user.password, current_password):
            raise WrongPassword

        # обновление hash-пароля
        data = {
            'password': self.generate_password(new_password)
        }
        self.dao.update_by_email(data, email)

    def generate_password(self, password: str) -> bytes:
        """Генерация пароля с 'SHA256'"""
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash: str, other_password: str) -> bool:
        """Сравнение переданного пароля с паролем пользователя в БД"""
        # декодирование пароля из базы данных
        decoded_digest = base64.b64decode(password_hash)

        # передача hash-пароля
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        is_equal = hmac.compare_digest(decoded_digest, hash_digest)  # compare_digest() - метод для сравнения паролей

        return is_equal
