from django.contrib import admin

from . import models
from .models import Post, Group, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    # will work for all columns: where empty - there will be this line " empty"
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author")
    list_filter = ("created",)
    empty_value_display = "-пусто-"
    search_fields = ("text",)


admin.site.register(Comment, CommentAdmin)