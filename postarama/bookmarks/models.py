from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class BookmarkManager(models.Manager):
    use_for_related_fields = True

    def posts(self):
        return self.get_queryset().filter(
            content_type__model='post').order_by('-post__updated')

    def get_bookmark_count(self):
        return self.get_queryset().all().count()


class Bookmark(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='bookmarks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = BookmarkManager()
