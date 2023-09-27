from django import template
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from bookmarks.models import Bookmark
from likes import services
from likes.models import Like
from posts.models import Post
from django.contrib.auth import get_user_model

from posts import views
from bookmarks import services

User = get_user_model()

register = template.Library()


# from_time = int(from_time)


@register.simple_tag
def search(request):
    """Получает всех пользователей, которые дизлайкнули `obj`.
    """
    query = views.post_search(request)
    return query


@register.filter
def str_to_int(some_string):
    return int(some_string)


@register.filter
def user_bookmarks(user):
    return user.bookmarks.filter()


@register.filter
def published_post_count(user):
    posts = Post.objects.published().filter(author=user).count()
    return posts
