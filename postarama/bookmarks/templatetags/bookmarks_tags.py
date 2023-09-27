from bookmarks import services
from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()


@register.simple_tag
def get_users_who_added_a_bookmark(obj):
    """Получает всех пользователей, которые добавили в закладки `obj`."""
    return services.get_users_who_added_a_bookmark(obj)
