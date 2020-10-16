from flask import request
from flask_restful import Resource

from models.db import db
from models.character import Character, CharacterSchema
from models.hat import Hat, HatSchema
import json
import re

Characters_schema = CharacterSchema(many=True)
CharacterSchema = CharacterSchema()

HatSchema = HatSchema(many=True)


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
            return 'No input data provided', 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Avoid printing a DB error to the user
        # Checks if the hat does exist
        user = Character.query.filter_by(id=data['id'])
        exist = Characters_schema.dump(user)

        if exist:
            return 'Character already exists', 400

        # the 1-1 relationship with the hat disable the possibility to create a character with hat = False
        if not data['human']:
            return 'can not create the character', 400

        # Weight and age constraint
        if data['weight'] > 80 and data['human'] == True:
            if data['age'] < 10:
                return 'weight is too big for age', 400

        # Age constraint
        if data['age'] < 0:
            return 'age is not correct', 400

        # p and yellow constraint
        hat = Hat.query.filter_by(id=data['hat'])
        hat = HatSchema.dump(hat)

        if (re.search('p', data['name']) or re.search('P', data['name'])) and hat[0]['colour'] == "YELLOW":
            return 'You have a p in your name, can not have a yellow hat', 400

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
            return 'No input data provided', 400

        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        user = Character.query.filter_by(id=data['id'])
        # Checks if the user does exist
        exist = Characters_schema.dump(user)
        if not exist:
            return 'Character already missing', 400

        user.delete()

        # db.session.delete(user)
        # Hat.query.filter_by(id=data['hat']).delete()

        db.session.commit()
        return {'User deleted ': data['id']}, 200

    @classmethod
    def put(cls):
        json_data = request.get_json(force=True)
        if not json_data:
            return 'No input data provided', 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Checks if the user does exist
        user = Character.query.filter_by(id=data['id'])
        exist = Characters_schema.dump(user)

        if not exist:
            return 'Character does not exist', 400

        # if data['weight'] > 80 and data['human'] == True:
        # if data['age'] < 10:
        # return 'weight is too big for age'
        # if data['age'] < 0:
        # return 'age is not correct'

        user = Character.query.filter_by(id=data['id']).update(data)

        db.session.commit()
        result = CharacterSchema.dump(user)
        return result, 201
