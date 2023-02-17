from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (
    CommentSerializer,
    FollowValidSerializer,
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
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ("user", "following")
    search_fields = ("following__username",)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        following = get_object_or_404(User, id=pk)
        data = {"user": user.id, "following": pk}
        serializer = FollowValidSerializer(
            data=data,
            context={"request": request, "following": following},
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            following = Follow.objects.create(user=user, following=following)
            return Response(
                serializer.to_representation(instance=following),
                status=status.HTTP_201_CREATED,
            )
        Follow.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        # print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = User.objects.filter(following__user=user)
        # print(queryset)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
    

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


class FollowViewSet123(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    # serializer_class = FollowValiSerializer
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ("user", "following")
    search_fields = ("following__username",)
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
