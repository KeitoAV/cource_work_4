from sqlalchemy import desc

from dao.model.movie import Movie
from utils import get_pagination


# класс с методами доступа к данным (Data Access Object)
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Movie).get(bid)

    def get_all(self, page, status):
        select = self.session.query(Movie)

        offs, lim = get_pagination(Movie, page)

        if status == 'new':
            select = select.order_by(desc(Movie.year))

        return select.limit(lim).offset(offs).all()

    # def get_all(self): # no pagination
    #     return self.session.query(Movie).all()
