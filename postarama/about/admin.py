from django.contrib import admin

from .models import Image, Technology


class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "image")


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Image, ImageAdmin)
admin.site.register(Technology, TechnologyAdmin)
