from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "updated", "status")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("-status", "-publish")

    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "description",
    )
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "text", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("author", "text")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("user", "author")
