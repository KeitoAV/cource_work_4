from sqlalchemy import desc

from dao.model.director import Director
from utils import get_pagination


# класс с методами доступа к данным (Data Access Object)
class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Director).get(bid)

    def get_all(self, page, status: None):
        select = self.session.query(Director)

        offs, lim = get_pagination(Director, page)

        if status == 'new':
            select = select.order_by(desc(Director.year))

        return select.limit(lim).offset(offs).all()
