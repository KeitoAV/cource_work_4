from dao.director import DirectorDAO
from dao.model.director import Director
from exceptions import PostNotFound


# класс для реализации бизнес логики
class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did: int):
        """Получить режиссера по ID"""
        director = self.dao.get_one(did)
        if not director:
            raise PostNotFound
        return director

    def get_all(self, page, status) -> list[Director]:
        """Получить всех режиссеров """
        directors = self.dao.get_all(page, status)
        if not directors:
            raise PostNotFound
        return directors

