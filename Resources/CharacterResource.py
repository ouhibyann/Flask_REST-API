from flask import request, jsonify
from flask_restful import Resource
from models.db import db
from models.character import Character, CharacterSchema
import json

Characters_schema = CharacterSchema(many=True)
CharacterSchema = CharacterSchema()


class CharacterResource(Resource):

    @staticmethod
    def get():
        users = Character.query.all()
        users = Characters_schema.dumps(users)
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
        # user = Character.query.get(id=data['id'])

        # if user:
            # return {'message': 'User already exists'}, 400

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
        user = Character.query.filter_by(id=data['id'])

        db.session.delete(user)
        db.session.commit()
        return 'User deleted', 200

    @staticmethod
    def put():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = CharacterSchema.loads(response)

        # Checks if the user does exist
        # get(id)
        user = Character.query.filter_by(id=data['id']).update(data)

        db.session.commit()
        result = CharacterSchema.dump(user)
        return result, 201