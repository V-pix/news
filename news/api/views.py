from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    ChanelSerializer,
    PostSerializer,
)
from posts.models import Comment, Follow, Chanel, Post, User


class ClassFollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (
        # permissions.IsAuthenticatedOrReadOnly,
        # IsAuthorOrReadOnlyPermission,
    # )
    pagination_class = LimitOffsetPagination
    
    
    def perform_create123(self, serializer):
        print(self.request)
        chanel = get_object_or_404(Chanel, pk=self.kwargs.get("chanel_id"))
        print(chanel)
        serializer.save(chanel_id=chanel.id)
    
    def perform_create123(self, request, serializer):
        if request.method == "POST":
            user = request.user
            if user.is_anonymous:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            chanel = get_object_or_404(Chanel, pk=self.kwargs.get("chanel_id"))
            serializer.save(chanel_id=chanel.id)


class ChanelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chanel.objects.all()
    serializer_class = ChanelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission,
    )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(post_id=post.id, author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()


class FollowViewSet(ClassFollowViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ("user", "following")
    search_fields = ("following__username",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()
