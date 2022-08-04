from dao.model.movie import Movie
from dao.movie import MovieDAO
from exceptions import PostNotFound


# класс для реализации бизнес логики
class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid: int):
        """Получить фильм по ID"""
        movie = self.dao.get_one(mid)
        if not movie:
            raise PostNotFound
        return movie

    def get_all(self, page, status) -> list[Movie]:
        """Получить все фильмы """
        movies = self.dao.get_all(page, status)
        if not movies:
            raise PostNotFound
        return movies


