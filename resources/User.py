from flask import request
from flask_restful import Resource, abort, reqparse
from model import db, User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'A user with this email already exist'}, 400
        user = User(
            name=json_data['name'],
            email=json_data['email'],
            password=json_data['password'],
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data
        del result['password']

        return {"status": 'success', 'data': result}, 201

    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200

    def put(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data, partial=True)
        if errors:
            return errors, 422
        user = User.query.get(user_id)
        if not user:
            return {'message': 'A user with that Id is not found'}, 400
        user.name = data['name']
        db.session.commit()

        result = user_schema.dump(user).data
        del result['password']

        return {"status": 'success', 'data': result}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'A user with that Id is not found'}, 400
        db.session.delete(user)
        db.session.commit()

        return {"status": 'success',  'message': 'User sucessfully deleted'},
        200

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'A user with that Id is not found'}, 400

        result = user_schema.dump(user).data
        del result['password']

        return {'status': 'success', 'data': result}, 200
