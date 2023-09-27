from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import Like

User = get_user_model()


def add_like(obj, user):
    """Сначала удаляет дизлайк, если он существует, а потом уже добавляет лайк
    """

    obj_type = ContentType.objects.get_for_model(obj)

    #  Если у обьекта уже есть дизлайк от нас удаляем
    #  если нет - ничего не делаем
    try:
        dislike = Like.objects.get(
            content_type=obj_type, object_id=obj.id, user=user,
            vote=Like.DISLIKE)

        if dislike:
            dislike.delete()
            return
    except ObjectDoesNotExist:
        pass

    #  Создаем обьект лайка
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user, vote=Like.LIKE)

    return like


def add_dislike(obj, user):
    """Сначала удаляет лайк, если он существует, а потом уже добавляет дизлайк
    """
    obj_type = ContentType.objects.get_for_model(obj)

    #  Если у обьекта уже есть лайк от нас удаляем
    #  если нет - ничего не делаем
    try:
        like = Like.objects.get(
            content_type=obj_type, object_id=obj.id, user=user, vote=Like.LIKE)
        if like:
            like.delete()
            return
    except ObjectDoesNotExist:
        pass

    #  Создаем обьект дизлайка
    dislike, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user, vote=Like.DISLIKE)

    return dislike


def is_fan(obj, user, vote) -> bool:
    """Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user, vote=vote)
    return likes.exists()


def get_fans(obj):
    """Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id,
        likes__vote=Like.LIKE)


def get_haters(obj):
    """Получает всех пользователей, которые дизлайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id,
        likes__vote=Like.DISLIKE)
