from flask import request
from flask_restful import Resource
from models.db import db
from models.hat import Hat, HatSchema
import json

Hats_schema = HatSchema(many=True)
HatSchema = HatSchema()


class HatOne(Resource):

    @staticmethod
    def get():
        json_data = request.get_json(force=True)

        user = Hat.query.filter_by(id=json_data['id'])
        user = Hats_schema.dump(user)
        return user, 200


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
        user = Hat.query.filter_by(id=data['id'])
        exist = Hats_schema.dump(user)
        if exist:
            return {'message': 'Hat already exists'}, 400

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

        # Checks if the hat does exist
        user = Hat.query.filter_by(id=data['id'])
        exist = Hats_schema.dump(user)

        if not exist:
            return 'Hat already missing', 400

        Hat.query.filter_by(id=data['id']).delete()

        db.session.commit()
        return {'Hat deleted': data['id']}, 200

    @staticmethod
    def put():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = HatSchema.loads(response)

        # Checks if the hat does exist
        user = Hat.query.filter_by(id=data['id'])
        exist = Hats_schema.dump(user)

        if not exist:
            return 'Hat does not exist', 400

        hat = Hat.query.filter_by(id=data['id'])
        hat.update(data)

        db.session.commit()
        result = HatSchema.dump(hat)
        return result, 201
