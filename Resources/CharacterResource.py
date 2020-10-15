from flask import request
from flask_restful import Resource

from models.hat import Hat
from models.db import db
from models.character import Character, CharacterSchema
import json
import re

Characters_schema = CharacterSchema(many=True)
CharacterSchema = CharacterSchema()


class CharacterOne(Resource):

    @classmethod
    def get(cls):
        json_data = request.get_json(force=True)

        user = Character.query.filter_by(id=json_data['id'])
        user = Characters_schema.dump(user)
        return user, 200


class CharacterResource(Resource):

    @classmethod
    def get(cls):
        users = Character.query.all()
        users = Characters_schema.dump(users)
        return users, 200

    @classmethod
    def post(cls):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Avoid printing a DB error to the user
        # Checks if the hat does exist
        user = Character.query.filter_by(id=data['id'])
        exist = Characters_schema.dump(user)

        if exist:
            return 'User already exists', 400

        # the 1-1 relationship with the hat disable the possibility to create a character with hat = False
        if not data['human']:
            return 'can not create the character'

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

    @classmethod
    def delete(cls):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Checks if the hat does exist
        user = Character.query.filter_by(id=data['id'])
        exist = Characters_schema.dump(user)
        if not exist:
            return 'Hat already missing', 400

        user.delete()
        # db.session.delete(user)
        # Hat.query.filter_by(id=data['hat']).delete()

        db.session.commit()
        return {'User deleted ': data['id']}, 200

    @classmethod
    def put(cls):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Checks if the user does exist
        user = Character.query.filter_by(id=data['id'])
        exist = Characters_schema.dump(user)

        if not exist:
            return 'Character does not exist', 400

        #if data['weight'] > 80 and data['human'] == True:
            #if data['age'] < 10:
                #return 'weight is too big for age'
        #if data['age'] < 0:
            #return 'age is not correct'

        # if re.search('[pP]', data['name']) and data['hat'] == "YELLOW":
        # return 'You have a p in your name, can not have a yelloy hat'

        user = Character.query.filter_by(id=data['id']).update(data)

        db.session.commit()
        result = CharacterSchema.dump(user)
        return result, 201
