from flask import request
from flask_restful import Resource

from src.models import Like, Session


class LikeAggregationResource(Resource):
    def get(self):
        date_from, date_to = request.args.get('date_from'), request.args.get('date_to')
        likes = Like.filter_by_date(date_from, date_to)
        return {"msg": f"Likes {likes}"}, 200


class UserAnalyticsResource(Resource):
    def get(self, user_id: int = None):
        last_time_logged_in = Session.get_last_login(user_id)
        return {"msg": f"Last time {user_id} was logged in {last_time_logged_in}"}, 200
