from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CHOICES = (
        ('Good', '👍'),
        ('Bad', '👎'),
        ('Shame', '🤦🏻‍♂'),
        ('Like', '❤️'),
        ('Fire', '🔥'),
    )

class Chanel(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название канала",
        help_text="Укажите название канала",
        unique=True,
    )
    avatar = models.ImageField(
        verbose_name="Аватарка", upload_to="avatars/", null=True, blank=True,
    )
    description = models.TextField(
        verbose_name="Описание канала",
        help_text="Укажите описание канала",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chanels",
        verbose_name="Автор",
    )
    
    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"
    
    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите текстовое описание",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
        db_index=True,
    )
    chanel = models.ForeignKey(
        Chanel,
        on_delete=models.CASCADE,
        related_name="posts",
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    
    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self) -> str:
        return f"{self.text}, {self.chanel}, {self.pk}"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    created = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True,
    )
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return f"{self.text}, {self.author}, {self.post.id}"


class Reply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="replies",
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies",
    )
    text = models.TextField(
        verbose_name="Текст ответа",
    )
    created = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True,
    )
    
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self) -> str:
        return f"{self.text}, {self.author}, {self.comment.id}"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_following"
            ),
            models.CheckConstraint(
                name="prevent_self_follow",
                check=~models.Q(user=models.F("following")),
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.user}, {self.following}"


class Reaction(models.Model):
    emoji = models.CharField(max_length=16, choices=CHOICES)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="reactions",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reactions",
    )
    
    class Meta:
        verbose_name = "Реакция"
        verbose_name_plural = "Реакции"

    def __str__(self )-> str:
        return self.emoji
