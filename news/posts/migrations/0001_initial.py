# Generated by Django 2.2.19 on 2023-02-15 06:04

import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chanel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Укажите название канала",
                        max_length=200,
                        unique=True,
                        verbose_name="Название канала",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="avatars/",
                        verbose_name="Аватарка",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Укажите описание канала",
                        verbose_name="Описание канала",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chanels",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Введите текстовое описание",
                        verbose_name="Текстовое описание",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "chanel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="posts.Chanel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "ordering": ("-pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follower",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Подписчик",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст комментария")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="posts.Post",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("user", "following"), name="unique_following"
            ),
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.CheckConstraint(
                check=models.Q(
                    _negated=True, user=django.db.models.expressions.F("following")
                ),
                name="prevent_self_follow",
            ),
        ),
    ]
