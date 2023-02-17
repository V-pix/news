from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsAuthorOrReadOnlyPermission, IsAuthorOrReadOnlyPermission1
from .serializers import (
    CommentSerializer,
    FollowValidSerializer,
    FollowSerializer,
    ChanelSerializer,
    PostSerializer,
    ReplySerializer,
    ReactionSerializer,
)
from posts.models import Comment, Follow, Chanel, Post, User, Reply, Reaction


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
    
    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated]
    )
    def reply123(self, request, pk, post_id):
        # print(request)
        user = request.user
        text = self.request.GET.get('text')
        # print(text)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        comment = get_object_or_404(Comment, id=pk)
        data = {"user": user.id, "comment": pk}
        serializer = ReplySerializer(
            data=data,
            context={"request": request, "comment": comment},
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            text = self.request.GET.get('text')
            print(text)
            comment = Reply.objects.create(user=user, text=text, comment=comment)
            return Response(
                serializer.to_representation(instance=comment),
                status=status.HTTP_201_CREATED,
            )
        Reply.objects.filter(user=user, comment=comment).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission,
    )

    def perform_create(self, serializer):
        # post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        serializer.save(comment_id=comment.id, author=self.request.user)

    def get_queryset(self):
        # post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        return comment.replies.all()


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission1,
    )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        # comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        serializer.save(post_id=post.id, user=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        # comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        return post.reactions.all()