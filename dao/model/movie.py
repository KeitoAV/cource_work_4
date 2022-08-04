from marshmallow import Schema, fields

from dao.model.director import DirectorSchema, Director
from dao.model.genre import GenreSchema, Genre
from setup_db import db


# модель SQLAlchemy для сущности
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    trailer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey(f"{Director.__tablename__}.id"), nullable=False)

    genre = db.relationship("Genre")
    director = db.relationship("Director")


# схема для сериализации
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()

    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)
