from django.contrib import admin

from .models import Chanel, Comment, Follow, Post, Reaction, Reply

admin.site.register(Chanel)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Reply)
admin.site.register(Reaction)
