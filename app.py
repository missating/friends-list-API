from flask import Blueprint
from flask_restful import Api
from resources.User import (UserRegistration, UserLogin, ViewAllUsers,
                            UpdateUser)


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserRegistration, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(ViewAllUsers, '/users')
# api.add_resource(UserResource, '/user/<user_id>', endpoint="user")
