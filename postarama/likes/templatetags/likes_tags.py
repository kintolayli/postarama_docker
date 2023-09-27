from django import template
from django.contrib.auth import get_user_model
from likes import services

User = get_user_model()

register = template.Library()


@register.simple_tag
def get_fans(obj):
    """Получает всех пользователей, которые лайкнули `obj`."""
    return services.get_fans(obj)


@register.simple_tag
def get_haters(obj):
    """Получает всех пользователей, которые дизлайкнули `obj`."""
    return services.get_haters(obj)


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False
