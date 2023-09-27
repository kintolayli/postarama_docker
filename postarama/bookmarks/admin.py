from django.contrib import admin
from bookmarks.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'content_object')
    search_fields = ('user', 'content_type')