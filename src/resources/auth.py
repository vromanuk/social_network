from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import bcrypt
from src.models import User

from src.services.auth_service import AuthService
from src.schemas import UserSchema, UserLoginSchema


class RegisterResource(Resource):
    def post(self):
        try:
            json_data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 422
        hashed_password = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
        user = User(username=json_data['username'], email=json_data['email'], password=hashed_password)
        AuthService.register(user)

        return {"msg": f"You have been registered. {user.username}"}, 201


class LoginResource(Resource):
    def post(self):
        try:
            json_data = UserLoginSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 422
        user = User.query.filter_by(email=json_data['email']).first()
        if user and bcrypt.check_password_hash(user.password, json_data['password']):
            AuthService.login(user)

        return {"msg": f"Logged in as {json_data['email']}."}, 200


class Logout(Resource):
    def get(self):
        AuthService.logout()

        return {"msg": "You have been logged out."}, 200
