import base64

from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from posts.models import (CHOICES, Chanel, Comment, Follow, Post, Reaction,
                          Reply)
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class ChanelSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)
    avatar = Base64ImageField(required=False, allow_null=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Chanel
        fields = (
            "id",
            "title",
            "avatar",
            "description",
            "author",
            "posts",
            "is_subscribed",
        )

    def get_is_subscribed(self, data):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context.get("request").user, following=data.id
        ).exists()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "text", "pub_date", "chanel", "author")
        model = Post
        read_only_field = ("author",)

    def validate(self, data):
        request = self.context.get("request")
        chanel = data["chanel"]
        user = self.context.get("request").user
        chanels = Chanel.objects.filter(author=user)
        if request.method == "POST":
            if chanel not in chanels:
                raise serializers.ValidationError("Нельзя выбрать чужой канал")
        if request.method == "PUT":
            if chanel not in chanels:
                raise PermissionDenied("Нельзя редактировать чужой пост")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author", "created", "post")


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    comment = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        fields = "__all__"
        model = Reply
        read_only_fields = ("author", "created", "comment", "post")


class FollowValidSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.PrimaryKeyRelatedField(
        queryset=Chanel.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        following = data["following"].id
        user = self.context.get("request").user
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == "POST":
            if user == following:
                raise serializers.ValidationError(
                    "Нельзя подписываться на самого себя."
                )
            if follow.exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого пользователя."
                )
        if request.method == "DELETE":
            if user == following:
                raise serializers.ValidationError(
                    "Нельзя подписываться от самого себя."
                )
            if not follow.exists():
                raise serializers.ValidationError(
                    "Вы не подписаны на этого автора."
                )
        return data


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.PrimaryKeyRelatedField(
        queryset=Chanel.objects.all()
    )

    class Meta:
        model = Follow
        fields = (
            "user",
            "following",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user,
            following=obj.following
        ).exists()


class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    post = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    emoji = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = "__all__"
        model = Reaction
        read_only_fields = ("user", "post")

    def create(self, validated_data):
        reaction = Reaction.objects.create(**validated_data)
        reaction.save()
        return reaction

    def validate(self, data):
        request = self.context.get("request")
        print(data)
        emoji = data["emoji"]
        user = self.context.get("request").user
        reaction = Reaction.objects.filter(user=user, emoji=emoji)
        if request.method == "POST":
            if reaction.exists():
                raise serializers.ValidationError(
                    "Вы уже отреагировали на этот пост."
                )
        if request.method == "DELETE":
            if not reaction.exists():
                raise serializers.ValidationError(
                    "Вы не реагировали не этот пост."
                )
        return data
