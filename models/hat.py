from models.db import db


class HatModel(db.Model):
    __tablename__ = "Hat"
    id = db.Column(db.Integer, primary_key=True)
    colour = db.Column(db.Enum)

