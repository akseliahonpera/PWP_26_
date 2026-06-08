'''
User resources
'''

from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen.database import User
from vainamoinen.utils import require_user, require_admin

class UserItem(Resource):
    '''
    Resource for a singular User object
    '''

    @require_user
    def get(self, user):
        '''
        Get a user, including their private information
        ---
        description: Get a user, including their private information
        security:
          - ApiKeyAuth: []
        parameters:
        - $ref: '#/components/parameters/user'
        responses:
          '200':
            description: All data of the chosen user
            content:
              application/json:
                example:
                  id: 1
                  username: lawnmowerman734
                  password: securelyHashedPassword
                  email: lawn@mower.fi
                  address: yard lane 71
                  phone_number: 112
                  description: Yeah I mow lawns very well
                  created: 2026-04-05 10:24:34.875360
          '404':
            description: User not found
          '403':
            description: Authentication was not sufficient for this call

        '''
        valid_true_values = ["true", "yes", "1"]
        include_jobs = False
        include_jobs_str = request.args.get('include_jobs', default="False", type=str).lower()
        if include_jobs_str in valid_true_values:
            include_jobs = True

        return User.serialize(user, include_jobs=include_jobs), 200

    @require_user
    def put(self, user):
        '''
        Update a user
        ---
        description: Replace a user with new values
        security:
          - ApiKeyAuth: []
        parameters:
        - $ref: '#/components/parameters/user'
        requestBody:
          description: JSON document that contains new data for the user
          content:
            application/json:
              schema:
                $ref: '#components/schemas/User'
              example:
                id: 1
                username: lawnmowing and plumbing inc
                password: newPassword
                email: lawn@mower.fi
                phone_number: 112
                description: I mow lawns and now plumbing as well
                created: 2026-04-05 12:24:34.875360
        responses:
          '204':
            description: User was updated successfully
          '400':
            description: Server couldn't validate the request
          '409':
            description: A conflict was raised when attempting to update user data
          '415':
            description: Provided media was not valid JSON
          '404':
            description: User not found
          '403':
            description: Authentication was not sufficient for this call
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        try:
            user.update(request.json)
        except IntegrityError as e:
            raise Conflict(
                description="Error in UserItem put."
            ) from e
        return Response(status=204)

    @require_user
    def delete(self, user):
        '''
        Delete a user
        ---
        description: Delete a user from the database
        security:
          - ApiKeyAuth: []
        parameters:
        - $ref: '#/components/parameters/user'
        responses:
          '204':
            description: User deleted successfully
          '409':
            description: A conflict was raised when attempting to delete user data
          '404':
            description: User not found
          '403':
            description: Authentication was not sufficient for this call
        '''
        try:
            user.delete()
        except IntegrityError as e:
            raise Conflict(
                description="Error in UserItem delete."
            ) from e
        return Response(status=204)

class PublicUserItem(Resource):
    '''
    Resource for a singular User item, uses a different serializer than the non-public
    version. This version does not include private information
    '''
    def get(self, user):
        '''
        Get a user, omitting private information
        ---
        description: Get a user, omitting their private information
        parameters:
        - $ref: '#/components/parameters/user'
        responses:
          '200':
            description: Only public data of the chosen user
            content:
              application/json:
                example:
                  id: 1
                  username: lawnmowerman734
                  email: lawn@mower.fi
                  description: Yeah I mow lawns very well
                  created: 2026-04-05 10:24:34.875360
          '404':
            description: User was not found  
        '''
        valid_true_values = ["true", "yes", "1"]
        include_jobs = False
        include_jobs_str = request.args.get('include_jobs', default="False", type=str).lower()
        if include_jobs_str in valid_true_values:
            include_jobs = True

        return User.serialize_public(user, include_jobs=include_jobs), 200



class UserCollection(Resource):
    '''
    Resource for UserCollection
    '''

    @require_admin
    def get(self):
        '''
        Get all users with private data, including passwords
        Never allow non-admins this data
        ---
        description: Get all users, including their private information
        security:
          - ApiKeyAuth: []
        responses:
          '200':
            description: All data of the chosen user
            content:
              application/json:
                example:
                - id: 1
                  username: lawnmowerman734
                  password: securelyHashedPassword
                  email: lawn@mower.fi
                  address: yard lane 71
                  phone_number: 112
                  description: Yeah I mow lawns very well
                  created: 2026-04-05 10:24:34.875360
                - id: 2
                  username: leaf_blower
                  password: qwerty12345
                  email: leafblower@pwp.fi
                  address: kaupungintalo 10
                  phone_number: 045 678 9012
                  description: leaf hehe
                  created: 2022-07-09 11:13:34.65536
          '403':
            description: Authentication was not sufficient for this call
        '''
        valid_true_values = ["true", "yes", "1"]
        include_jobs = False
        include_jobs_str = request.args.get('include_jobs', default="False", type=str).lower()
        if include_jobs_str in valid_true_values:
            include_jobs = True

        users = User.query_all(include_jobs=include_jobs)
        return users

    # TODO: Somehow force user API key initialization when a new user is added
    def post(self):
        '''
        Add a new user
        ---
        description: Add a new user to the database
        requestBody:
          description: JSON document that contains new data for the user
          content:
            application/json:
              schema:
                $ref: '#components/schemas/User'
              example:
                id: 1
                username: lawnmowing and plumbing inc
                password: newPassword
                email: lawn@mower.fi
                phone_number: 112
                description: I mow lawns and now plumbing as well
                created: 2026-04-05 12:24:34.875360
        responses:
          '201':
            description: User was created and uploaded successfully
            headers:
              Location:
                description: URL of the newly created job resource
                schema:
                  type: string
                  format: uri
          '400':
            description: Server couldn't validate the request
          '409':
            description: A conflict was raised when attempting to add the new user
          '415':
            description: Provided media was not valid JSON
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        try:
            user = User.insert(request.json)
        except IntegrityError as e:
            raise Conflict(
                description="Error in UserCollection post."
            ) from e
        return Response(status=201, headers={"Location":url_for("api.useritem", user=user)})

class PublicUserCollection(Resource):
    '''
    Resource for UserCollection
    Does not include private information
    '''

    def get(self):
        '''
        Get all users with public data
        ---
        description: Get all users, omitting their private information
        responses:
          '200':
            description: Only public data of the chosen user
            content:
              application/json:
                example:
                - id: 1
                  username: lawnmowerman734
                  email: lawn@mower.fi
                  description: Yeah I mow lawns very well
                  created: 2026-04-05 10:24:34.875360
                - id: 2
                  username: finnairpilot
                  email: finnair@gmail.fi
                  description: I offer plane and aviation services
                  created: 2025-01-09 11:19:34.783506

        '''
        valid_true_values = ["true", "yes", "1"]
        include_jobs = False
        include_jobs_str = request.args.get('include_jobs', default="False", type=str).lower()
        if include_jobs_str in valid_true_values:
            include_jobs = True

        # Note, never EVER omit the public parameter or change it to false
        # unless you want lawsuits to appear
        users = User.query_all(public=True, include_jobs=include_jobs)

        return users
