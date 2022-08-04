from dao.genre import GenreDAO
from dao.model.genre import Genre
from exceptions import PostNotFound


# класс для реализации бизнес логики
class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid: int):
        """Получить жанр по ID"""
        genre = self.dao.get_one(gid)
        if not genre:
            raise PostNotFound
        return genre

    def get_all(self, page, status) -> list[Genre]:
        """Получить все жанры """
        genres = self.dao.get_all(page, status)
        if not genres:
            raise PostNotFound
        return genres
