from flask import request
from flask_restful import Resource, abort, reqparse
from model import db, User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    """Handles user registration"""

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'status': 'fail',
                'data': {
                    'message': 'No data provided'
                }
            }, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with the email already exist'
                }
            }, 400
        user = User(
            name=json_data['name'],
            email=json_data['email'],
            password=json_data['password'],
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data
        del result['password']

        return {
            'status': 'success',
            'data': result
        }, 201

    """Handles user login"""

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'status': 'fail',
                'data': {
                    'message': 'No data provided'
                }
            }, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data, partial=True)
        if errors:
            return errors, 422

        user = User.query.filter_by(email=data['email']).first()
        if user and user.password_is_valid(password=data['password']):
            result = user_schema.dump(user).data
            del result['password']

            return {
                'status': 'success',
                'data': result
            }, 200
        else:
            return {
                'status': 'fail',
                'data': {
                    'message': 'Invalid email or password'
                }
            }, 400

    """Handles view all users"""

    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {
            'status': 'success',
            'data': users
        }, 200

    """Handles edit a single user"""

    def put(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'status': 'fail',
                'data': {
                    'message': 'No data provided'
                }
            }, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data, partial=True)
        if errors:
            return errors, 422

        user = User.query.get(user_id)
        if not user:
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with that id is not found'
                }
            }, 400
        user.name = data['name']
        db.session.commit()

        result = user_schema.dump(user).data
        del result['password']

        return {
            'status': 'success',
            'data': result
        }, 200

    """Handles delete a single user"""

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with that id does is not found'
                }
            }, 400
        db.session.delete(user)
        db.session.commit()

        return {
            'status': 'success',
            'data': {
                'message': 'User sucessfully deleted'
            }
        }, 200

    """Handles get a single user"""

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with that id is not found'
                }
            }, 400

        result = user_schema.dump(user).data
        del result['password']

        return {
            'status': 'success',
            'data': result
        }, 200
