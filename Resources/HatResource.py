from flask import request
from flask_restful import Resource
from models.db import db
from models.hat import Hat, HatSchema
import json

Hats_schema = HatSchema(many=True)
HatSchema = HatSchema()


class HatResource(Resource):

    @staticmethod
    def get():
        users = Hat.query.all()
        users = Hats_schema.dump(users)
        return users, 200

    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = HatSchema.loads(response)


        # Avoid printing a DB error to the user
        # user = Character.query.get(id=data['id'])

        # if user:
            # return {'message': 'User already exists'}, 400

        hat = Hat(
            id=data['id'],
            colour=data['colour']
        )

        db.session.add(hat)
        db.session.commit()
        result = HatSchema.dump(hat)
        return result, 201

    @staticmethod
    def delete():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = HatSchema.loads(response)
        hat = Hat.query.filter_by(id=data['id']).delete()

        db.session.commit()
        return {'User deleted': hat}, 200

    @staticmethod
    def put():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = HatSchema.loads(response)

        # Checks if the user does exist
        # get(id)
        hat = Hat.query.filter_by(id=data['id']).update(data)

        db.session.commit()
        result = HatSchema.dump(hat)
        return result, 201