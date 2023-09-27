from django import template
from django.contrib.auth import get_user_model
from posts import views
from posts.models import Post

User = get_user_model()

register = template.Library()


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
