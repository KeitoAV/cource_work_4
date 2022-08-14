from constants import LIMIT
from dao.model.user import User


def get_pagination(model, page):
    """Пагинация страниц"""
    try:
        page = int(page)
        limitation = LIMIT
    except (TypeError, ValueError):
        page = 1
        limitation = model.query.count()

    offset = (page - 1) * limitation
    return offset, limitation


def create_data(app, db):
    """Наполнение таблицы User данными"""
    with app.app_context():
        db.create_all()

        u1 = User(email="olga@ya.ru", password="olga1", name=None, surname=None, favourite_genre=None)

        with db.session.begin():
            db.session.add_all([u1])








#         u1 = User(name="polina", password="polina2", email="polina@ya.ru", surname="ivanova")
#         u2 = User(name="emilia", password="emilia2", email="emilia@ya.ru", surname="valeeva")
#         u3 = User(name="olga", password="olga1", email="olga@ya.ru", surname="orlova")
#         u4 = User(name="keito", password="keito1", email="keito@ya.ru", surname="valeeva")
