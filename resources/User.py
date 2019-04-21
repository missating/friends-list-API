from flask import request
from flask_restful import Resource, abort
from model import db, User, UserSchema
from flask_jwt_extended import (create_access_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRegistration(Resource):
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

        try:
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=data['email'])
            result = user_schema.dump(user).data
            del result['password']

            return {
                'status': 'success',
                'data': result,
                'access_token': access_token,
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
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
            access_token = create_access_token(identity=data['email'])

            result = user_schema.dump(user).data
            del result['password']

            return {
                'status': 'success',
                'data': result,
                'access_token': access_token,
            }, 200
        else:
            return {
                'status': 'fail',
                'data': {
                    'message': 'Invalid email or password'
                }
            }, 400


class ViewAllUsers(Resource):
    """Handles view all users"""

    @jwt_required
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data

        for user in users:
            del user['password']

        return {
            'status': 'success',
            'data': users
        }, 200


class UpdateUser(Resource):
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


class DeleteUser(Resource):
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


class ViewAUser(Resource):
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
