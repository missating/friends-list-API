from flask import Blueprint
from flask_restful import Api
from resources.User import (UserRegistration, UserLogin, ViewAllUsers,
                            UpdateUser, DeleteUser, ViewAUser)
from resources.Friend import AddFriend

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserRegistration, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(ViewAllUsers, '/user')
api.add_resource(UpdateUser, '/user/<user_id>')
api.add_resource(DeleteUser, '/user/<user_id>')
api.add_resource(ViewAUser, '/user/<user_id>')
api.add_resource(AddFriend, '/friend')
