from flask import jsonify, request
from flask_restful import Resource
from model import db, Friend, User, FriendSchema

friends_schema = FriendSchema(many=True)
friend_schema = FriendSchema()


class AddFriend(Resource):
    """Handles adding of a friend by a registered user """

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
        data, errors = friend_schema.load(json_data, partial=True)
        if errors:
            return errors, 422
        user = User.query.filter_by(id=data['user_id']).first()
        if not user:
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with that is not found'
                }
            }
        friend = Friend(
            user_id=json_data['user_id'],
            name=json_data['name'],
            age=json_data['age']
        )
        db.session.add(friend)
        db.session.commit()

        result = friend_schema.dump(friend).data

        return {
            'status': "success",
            'data': result
        }, 201


class GetAUserFriends(Resource):
    """Handles request to view a user friend list"""

    def get(self, user_id):
        friends = Friend.query.filter_by(user_id=user_id)

        result = friends_schema.dump(friends).data
        if not len(result):
            return {
                'status': 'fail',
                'data': {
                    'message': 'A user with that id is not found'
                }
            }, 400

        return {
            'status': 'success',
            'data': result
        }, 200
