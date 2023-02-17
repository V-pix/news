from django.urls import include, path
from rest_framework import routers

from .views import (
    CommentViewSet,
    ChanelViewSet,
    PostViewSet,
    ReplyViewSet,
    ReactionViewSet,
)

app_name = "api"

router_v1 = routers.DefaultRouter()

router_v1.register("posts", PostViewSet)
router_v1.register("chanels", ChanelViewSet)
router_v1.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)
router_v1.register(
    r"posts/(?P<post_id>\d+)/reactions", ReactionViewSet, basename="reactions"
)
router_v1.register(
    r"posts/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)/replies",
    ReplyViewSet,
    basename="replies",
)
# router_v1.register("follow", FollowViewSet)

urlpatterns = [
    path(
        "v1/users/subscriptions/",
        ChanelViewSet.as_view(
            {
                "get": "subscriptions",
            }
        ),
        name="subscriptions",
    ),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router_v1.urls)),
]
