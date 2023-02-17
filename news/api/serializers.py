from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import PermissionDenied


from posts.models import Comment, Follow, Chanel, Post, User


class ChanelSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Chanel
        fields = ("id", "title", "avatar", "description", "author", "posts", "is_subscribed",)
    
    def get_is_subscribed(self, data):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(user=user, author=data).exists()


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


class FollowValidSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.PrimaryKeyRelatedField(queryset=Chanel.objects.all())

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
                    "Вы уже подписаны на этого пользователя"
                )
        if request.method == "DELETE":
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
    following = serializers.PrimaryKeyRelatedField(queryset=Chanel.objects.all())

    class Meta:
        model = Follow
        fields = ("user", "following", "is_subscribed",)
        
    def get_is_subscribed(self, following):
        return Follow.objects.filter(
            user=self.context.get("request").user, following=following
        ).exists()
        
    def to_representation(self, instance):
        print(type(instance))
        # representation = super().to_representation(instance)
        print(instance)
        return FollowSerializer(
            context={"request": self.context.get("request")}
        ).data
