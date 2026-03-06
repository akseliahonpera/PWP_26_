from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen import Database, cache


class UserItem(Resource):
    
    '''
    Get a user
    '''
    @cache.cached()
    def get(self, user):
        return Database.User.serialize(user)

    '''
    Update a user
    '''
    def put(self, user):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            Database.update_user(user, request.json)
        except IntegrityError:
            raise Conflict(
                description="Something shitty happened"
            )
        return Response(status=204)

    '''
    
    ''' # unnecessary method? collection has post
    def post(self, user):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            Database.insertUser(request.json)
        except IntegrityError:
            raise Conflict(
                description="User with name '{username}' already in service".format(
                    **request.json
                )
            )
        return Response(status=204)

    '''
    Delete a user
    '''
    def delete(self, user):
        if Database.delete_user(user):
            return Response(status=204)
        return Response(status=400)


class UserCollection(Resource):

    '''
    Get all users
    '''
    def get(self):
        users = Database.query_user_all()
        return users

    '''
    Add a new user
    '''
    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            user = Database.insertUser(request.json)
        except IntegrityError:
            raise Conflict(
                description="User with name '{username}' already in service".format(
                    **request.json
                )
            )
        return Response(status=201, headers={"Location":url_for("api.useritem", user=user)})
