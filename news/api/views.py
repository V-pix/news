from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
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
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission,
    )
    pagination_class = LimitOffsetPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ChanelViewSet(viewsets.ModelViewSet):
    queryset = Chanel.objects.all()
    serializer_class = ChanelSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ("user", "following")
    search_fields = ("following__username",)
    # permission_classes = permissions.IsAuthenticatedOrReadOnly
    # permission_classes = (
        # permissions.IsAuthenticatedOrReadOnly,
        # IsAuthorOrReadOnlyPermission,
    # )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()
    
    @action(methods=['delete'], detail=True)
    def deletewesf(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        request = self.context.get("request")
        following = request["following"].id
        user = self.context.get("request").user
        author = get_object_or_404(User, id=following)
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy123(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy123(self, instance):
        instance.delete()
