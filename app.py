from flask import Blueprint
from flask_restful import Api
from resources.User import (UserRegistration, UserLogin, ViewAllUsers,
                            UpdateUser, DeleteUser, ViewAUser)
from resources.Friend import (AddFriend, GetAUserFriends)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserRegistration, '/users/register')
api.add_resource(UserLogin, '/users/login')
api.add_resource(ViewAllUsers, '/users')
api.add_resource(UpdateUser, '/users/<user_id>')
api.add_resource(DeleteUser, '/users/<user_id>')
api.add_resource(ViewAUser, '/users/<user_id>')
api.add_resource(AddFriend, '/friends')
api.add_resource(GetAUserFriends, '/friends/<user_id>')
