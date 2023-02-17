from django.contrib import admin

from .models import Chanel, Post, Comment, Follow, Reply, Reaction

admin.site.register(Chanel)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Reply)
admin.site.register(Reaction)


