# Generated by Django 2.2.19 on 2023-02-17 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0003_post_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="chanel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="posts.Chanel",
            ),
        ),
        migrations.CreateModel(
            name="Reply",
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
                ("text", models.TextField(verbose_name="Текст ответа")),
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
                        related_name="replies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="posts.Comment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ответ",
                "verbose_name_plural": "Ответы",
            },
        ),
    ]
