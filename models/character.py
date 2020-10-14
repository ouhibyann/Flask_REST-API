from models.db import db, ma
from marshmallow import fields


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    human = db.Column(db.Boolean)
    hat = db.Column(db.Integer)

    def __init__(self, id, name, age, weight, human, hat):
        self.id = id
        self.name = name
        self.age = age
        self.weight = weight
        self.human = human
        self.hat = hat


class CharacterSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    weight = fields.Float()
    human = fields.Boolean()
    hat = fields.Integer()



