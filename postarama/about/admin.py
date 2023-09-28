from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


admin.site.register(Image, ImageAdmin)