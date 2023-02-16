from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, ChanelViewSet, PostViewSet

app_name = "api"

router_v1 = routers.DefaultRouter()

router_v1.register("posts", PostViewSet)
router_v1.register("chanels", ChanelViewSet)
router_v1.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)
router_v1.register("follow", FollowViewSet)

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router_v1.urls)),
]