from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class PostSchema(Schema):
    title = fields.String(required=True)
    content = fields.String(required=True)
    date_posted = fields.DateTime(required=False)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
