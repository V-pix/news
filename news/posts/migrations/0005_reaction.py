# Generated by Django 2.2.19 on 2023-02-17 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0004_auto_20230217_0953"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reaction",
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
                    "emoji",
                    models.CharField(
                        choices=[
                            ("Good", "👍"),
                            ("Bad", "👎"),
                            ("Shame", "🤦🏻\u200d♂"),
                            ("Like", "❤️"),
                            ("Fire", "🔥"),
                        ],
                        max_length=16,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to="posts.Post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]