from marshmallow import Schema, fields

from dao.model.genre import Genre, GenreSchema
from setup_db import db


# модель SQLAlchemy для сущности
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favourite_genre = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"))

    genre = db.relationship("Genre")


# схема для сериализации
class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str(load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favourite_genre = fields.Int()

    genre = fields.Nested(GenreSchema)


