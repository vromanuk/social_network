from src import api
from src.resources.auth import RegisterResource, LoginResource
from src.resources.likes import LikeAggregationResource
from src.resources.posts import PostResource, LikePostResource
from src.resources.smoke import Smoke
from src.resources.users import UserResource

api.add_resource(Smoke, '/smoke', strict_slashes=False)

api.add_resource(UserResource, '/users/<int:user_id>/posts', '/users/<int:user_id>/posts/<int:post_id>',
                 strict_slashes=False)
api.add_resource(PostResource, '/posts', '/posts/<int:post_id>', strict_slashes=False)
api.add_resource(LikePostResource, '/posts/<int:post_id>/like', '/posts/<int:post_id>/dislike', strict_slashes=False)
api.add_resource(LikeAggregationResource, '/api/analytics', strict_slashes=False)

api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
