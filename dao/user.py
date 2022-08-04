from sqlalchemy import desc
from dao.model.user import User
from utils import get_pagination


# класс с методами доступа к данным (Data Access Object)
class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one()

    def get_all(self, page, status: None):
        select = self.session.query(User)

        offs, lim = get_pagination(User, page)

        if status == 'new':
            select = select.order_by(desc(User.year))

        return select.limit(lim).offset(offs).all()

    def create(self, user_d):
        user = User(**user_d)
        self.session.add(user)
        self.session.commit()
        return user

    def update_by_email(self, data, email):
        self.session.query(User).filter(User.email == email).update(data)
        self.session.commit()
