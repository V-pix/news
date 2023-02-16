from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Chanel, Post, User


class ChanelSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Chanel
        fields = ("id", "title", "avatar", "description", "author", "posts")
        # read_only_field = ("slug",)


class PostSerializer(serializers.ModelSerializer):
    # chanel = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ("id", "text", "pub_date", "chanel")
        model = Post
        # read_only_field = ("pub_date", "chanel",)
        read_only_field = ("chanel",)
    
    def create(self, validated_data):
        print(self.initial_data)
        print(self.validated_data)
        chanel = validated_data.pop("chanel")
        post = Post.objects.create(
            chanel=chanel, **validated_data
        )
        post.save()
        return post


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
        if self.context.get("request").user == following:
            raise serializers.ValidationError(
                "Нельзя подписываться на самого себя"
            )
        return following

    class Meta:
        model = Follow
        fields = ("user", "following")

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]
