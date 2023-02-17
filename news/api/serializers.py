from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import PermissionDenied


from posts.models import Comment, Follow, Chanel, Post, User


class ChanelSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Chanel
        fields = ("id", "title", "avatar", "description", "author", "posts")


class PostSerializer(serializers.ModelSerializer):
    # chanel = serializers.StringRelatedField(read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "text", "pub_date", "chanel", "author")
        model = Post
        read_only_field = ("author",)
        # read_only_field = ("pub_date", "chanel",)
        
    def validate(self, data):
        request = self.context.get("request")
        chanel = data["chanel"]
        user = self.context.get("request").user
        chanels = Chanel.objects.filter(author=user)
        if request.method == "POST":
            if chanel not in chanels:
                raise serializers.ValidationError(
                    "Нельзя выбрать чужой канал"
                )
        if request.method == "PUT":
            if chanel not in chanels:
                raise PermissionDenied(
                    "Нельзя редактировать чужой пост"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author", "created", "post")


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )
    
    def validate_following(self, following):
        user = self.context.get("request").user
        follow = Follow.objects.filter(user=user, following=following)
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписываться на самого себя"
            )
        if follow.exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого пользователя"
                )
        return following
    
    def validate(self, data):
        request = self.context.get("request")
        following = data["following"].id
        user = self.context.get("request").user
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == "DELETE":
            if not follow.exists():
                raise serializers.ValidationError(
                    "Вы не подписаны на этого автора."
                )
        return data

    class Meta:
        model = Follow
        fields = ("user", "following")

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]
