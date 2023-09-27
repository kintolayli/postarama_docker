from django.contrib import admin
from likes.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "vote",
        "content_type",
        "object_id",
        "content_object",
    )
    search_fields = ("user", "content_type")
