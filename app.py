from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserResource, '/user/register', endpoint="register_user")
api.add_resource(UserResource, '/user/login', endpoint="login_user")
api.add_resource(UserResource, '/user', endpoint="users")
api.add_resource(UserResource, '/user/<user_id>', endpoint="user")
