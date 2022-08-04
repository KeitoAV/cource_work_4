from marshmallow import Schema, fields

from setup_db import db


# модель SQLAlchemy для сущности
class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)


# схема для сериализации
class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
