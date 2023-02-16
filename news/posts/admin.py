from django.contrib import admin

from .models import Chanel, Post, Comment, Follow

admin.site.register(Chanel)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Follow)

