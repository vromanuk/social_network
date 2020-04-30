from flask import request
from flask_restful import Resource

from src.models import Like


class LikeAggregationResource(Resource):
    def get(self):
        date_from, date_to = request.args.get('date_from'), request.args.get('date_to')
        likes = Like.filter_by_date(date_from, date_to)
        return {"msg": f"Likes {likes}"}, 200
