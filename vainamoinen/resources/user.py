'''
User resources
'''

from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen.database import User


class UserItem(Resource):

    def get(self, user):
        '''
        Get a user
        '''
        return User.serialize(user)

    def put(self, user):
        '''
        Update a user
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            user.update(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in UserItem put."
            )
        return Response(status=204)

    def delete(self, user):
        '''
        Delete a user
        '''
        try:
            user.delete()
        except IntegrityError:
            raise Conflict(
                description="Error in UserItem delete."
            )
        return Response(status=204)


class UserCollection(Resource):

    def get(self):
        '''
        Get all users
        '''
        return User.query_all()

    def post(self):
        '''
        Add a new user
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            user = User.insert(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in UserCollection post."
            )
        return Response(status=201, headers={"Location":url_for("api.useritem", user=user)})
