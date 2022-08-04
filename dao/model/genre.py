from marshmallow import Schema, fields

from setup_db import db


# модель SQLAlchemy для сущности
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# схема для сериализации
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
