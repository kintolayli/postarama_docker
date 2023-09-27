from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum

User = get_user_model()


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum("vote")).get("vote__sum") or 0

    def posts(self):
        return (
            self.get_queryset()
            .filter(content_type__model="post")
            .order_by("-post__updated")
        )

    def comments(self):
        return (
            self.get_queryset()
            .filter(content_type__model="comment")
            .order_by("-comments__updated")
        )


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = ((DISLIKE, "Не нравится"), (LIKE, "Нравится"))
    vote = models.SmallIntegerField(choices=VOTES)

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = LikeManager()
