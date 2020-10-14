from models.db import db
from flask import Flask, Blueprint
from flask_restful import Api
from Resources.CharacterResource import CharacterResource, CharacterOne
from Resources.HatResource import HatResource, HatOne

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/Metron"

api_bp = Blueprint('api', __name__)
API = Api(api_bp)

API.add_resource(CharacterResource, '/character')
API.add_resource(HatResource, '/hat')
API.add_resource(CharacterOne, '/oneCharacter')
API.add_resource(HatOne, '/oneHat')

app.register_blueprint(api_bp)

if __name__ == '__main__':
    db.init_app(app)
    app.run()
