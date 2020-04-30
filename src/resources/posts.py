from flask import request
from flask_restful import Resource

from src import db
from src.models import Post, Like


class PostResource(Resource):
    def get(self, post_id: int = None):
        if not post_id:
            posts = Post.query.all()
        else:
            posts = Post.query.get(post_id)

        return posts, 200


class LikePostResource(Resource):
    def get(self, post_id: int = None):
        if not request.args:
            likes = Like.sum_likes_by_post(post_id)
        else:
            date_from, date_to = request.args.get('date_from'), request.args.get('date_to')
            likes = Like.filter_by_date_and_post(post_id, date_from, date_to)
        return {"msg": f"Likes {likes}"}, 200

    def post(self, post_id: int = None):
        post = Post.query.get(post_id)
        if request.path.split('/')[-1] == 'dislike':
            like = Like(likes=-1, post=post)
            msg = "Disliked"
        else:
            like = Like(post=post)
            msg = "Liked"

        db.session.add(like)
        db.session.commit()

        return {"msg": f"{msg} {post.title}"}, 201
