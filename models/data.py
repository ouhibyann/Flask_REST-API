from models.db import db, ma
from marshmallow import fields


class Data(db.Model):
    __tablename__ = "Data"
    Id = db.Column(db.Integer, primary_key=True)
    Created_date = db.Column(db.Date)
    Name = db.Column(db.String(128))
    Value = db.Column(db.Float)

    def __init__(self, Id, Created_date, Name, Value):
        self.Id = Id
        self.Created_date = Created_date
        self.Name = Name
        self.Value = Value


class DataSchema(ma.Schema):
    Id = fields.Integer()
    Created_date = fields.Date()
    Name = fields.String()
    Value = fields.Float()
