from flask import request
from flask_restful import Resource

from Resources.HatResource import HatOne
from models.db import db
from models.character import Character, CharacterSchema
import json
import re

Characters_schema = CharacterSchema(many=True)
CharacterSchema = CharacterSchema()


class CharacterOne(Resource):

    @staticmethod
    def get():
        json_data = request.get_json(force=True)

        user = Character.query.filter_by(id=json_data['id'])
        user = Characters_schema.dump(user)
        return user, 200


class CharacterResource(Resource):

    @staticmethod
    def get():
        users = Character.query.all()
        users = Characters_schema.dump(users)
        return users, 200

    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Avoid printing a DB error to the user
        # user = Character.query.filter_by(id=data['id'])
        # if user:
            # return {'message': 'User already exists'}, 400

        # if not data['human']:
        # data['hat'] = "0"

        if data['weight'] > 80 and data['human'] == True:
            if data['age'] < 10:
                return 'weight is too big for age'
        if data['age'] < 0:
            return 'age is not correct'

        user = Character(
            id=data['id'],
            name=data['name'],
            age=data['age'],
            weight=data['weight'],
            human=data['human'],
            hat=data['hat']
        )

        db.session.add(user)
        db.session.commit()
        result = CharacterSchema.dump(user)
        return result, 201

    @staticmethod
    def delete():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)
        user = Character.query.filter_by(id=data['id']).delete()

        db.session.commit()
        return {'User deleted': user}, 200

    @staticmethod
    def put():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # if not data['human']:
        #    data['hat'] = "0"

        if data['weight'] > 80 and data['human'] == True:
            if data['age'] < 10:
                return 'weight is too big for age'
        if data['age'] < 0:
            return 'age is not correct'

        #if re.search('[pP]', data['name']) and data['hat'] == "YELLOW":
            #return 'You have a p in your name, can not have a yelloy hat'

        # Checks if the user does exist
        # get(id)
        user = Character.query.filter_by(id=data['id']).update(data)

        db.session.commit()
        result = CharacterSchema.dump(user)
        return result, 201
