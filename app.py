from instance.config import app_config
from models.db import db
from flask import Flask, Blueprint
from flask_restful import Api
from Resources.CharacterResource import CharacterResource, CharacterOne
from Resources.HatResource import HatResource, HatOne


# app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/Metron"

api_bp = Blueprint('api', __name__)
API = Api(api_bp)

API.add_resource(CharacterResource, '/character')
API.add_resource(HatResource, '/hat')
API.add_resource(CharacterOne, '/oneCharacter')
API.add_resource(HatOne, '/oneHat')


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(api_bp)

    db.init_app(app)

    return app
'''
if __name__ == '__main__':
    db.init_app(app)
    app.run()
'''