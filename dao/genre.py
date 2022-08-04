from sqlalchemy import desc

from dao.model.genre import Genre
from utils import get_pagination


# класс с методами доступа к данным (Data Access Object)
class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Genre).get(bid)

    def get_all(self, page, status: None):
        select = self.session.query(Genre)

        offs, lim = get_pagination(Genre, page)

        if status == 'new':
            select = select.order_by(desc(Genre.year))

        return select.limit(lim).offset(offs).all()
