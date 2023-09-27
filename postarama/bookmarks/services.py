from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Bookmark

User = get_user_model()


def has_a_bookmark(obj, user) -> bool:
    """Проверяет, добавил ли в закладки `user` `obj`."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    bookmarks = Bookmark.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return bookmarks.exists()


def add_bookmark(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)

    #  Создаем обьект закладки
    bookmark, is_created = Bookmark.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user
    )

    return bookmark


def remove_bookmark(obj, user):
    """Удаляет закладку с `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Bookmark.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def get_users_who_added_a_bookmark(obj):
    """Получает всех пользователей, которые дизлайкнули `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        bookmarks__content_type=obj_type, bookmarks__object_id=obj.id
    )
