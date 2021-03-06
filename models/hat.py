from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models.db import db, ma
from marshmallow import fields
from marshmallow_enum import EnumField
from enum import Enum


class Colour(Enum):
    PURPLE = "PURPLE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Hat(db.Model):
    __tablename__ = "hat"
    id = db.Column(db.Integer, primary_key=True)
    colour = db.Column(db.Enum(Colour))
    char_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    # Creates the one to one relationship
    character = db.relationship("Character", backref=db.backref("children", cascade="all,delete", passive_deletes=True))

    def __init__(self, id, colour):
        self.id = id
        self.colour = colour


class HatSchema(ma.Schema):
    id = fields.Integer()
    colour = EnumField(Colour)  # by_value=True
