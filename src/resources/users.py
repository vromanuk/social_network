from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.models import User, Post
from src.schemas import PostSchema


class UserResource(Resource):
    def get(self, user_id: int = None, post_id: int = None):
        if not post_id:
            posts = Post.query.filter(user_id == Post.user_id).all()
        else:
            posts = Post.query. \
                filter(user_id == Post.user_id). \
                filter(post_id == Post.id)

        schema = PostSchema(many=True)
        result = schema.dump(posts)

        return result, 200

    def post(self, user_id: int = None):
        try:
            json_data = PostSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 422
        user = User.query.get(user_id)
        post = Post(title=json_data['title'], content=json_data['content'], author=user)
        db.session.add(post)
        db.session.commit()

        return {"msg": f"Post {post.title} created."}, 201
