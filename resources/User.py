from flask import request
from flask_restful import Resource
from model import db, User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    def get_user(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200
