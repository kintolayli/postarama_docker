from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from likes.models import Like
from likes.services import add_dislike, add_like, is_fan
from posts.models import Comment, Post

User = get_user_model()

RATING_UP_MESSAGE = "Вы увеличили рейтинг публикации"
RATING_DOWN_MESSAGE = "Вы понизили рейтинг публикации"


class PostRatingUpDown(LoginRequiredMixin, View):
    vote_type = None  # Тип Like/Dislike

    def post(self, request, username, post_id):
        obj = get_object_or_404(Post, author__username=username, pk=post_id)
        user = request.user

        if self.vote_type == Like.LIKE:
            add_like(obj, user)
        elif self.vote_type == Like.DISLIKE:
            add_dislike(obj, user)

        user_is_fan = is_fan(obj, user, Like.LIKE)
        user_is_hater = is_fan(obj, user, Like.DISLIKE)

        return JsonResponse(
            {
                "sum_rating": obj.likes.sum_rating(),
                "user_is_fan": user_is_fan,
                "user_is_hater": user_is_hater,
            },
            status=200,
        )


class CommentRatingUpDown(LoginRequiredMixin, View):
    vote_type = None  # Тип Like/Dislike

    def post(self, request, username, post_id, comment_id):
        obj = get_object_or_404(Comment, post=post_id, pk=comment_id)
        user = request.user

        if self.vote_type == Like.LIKE:
            add_like(obj, user)
        elif self.vote_type == Like.DISLIKE:
            add_dislike(obj, user)

        user_is_fan = is_fan(obj, user, Like.LIKE)
        user_is_hater = is_fan(obj, user, Like.DISLIKE)

        return JsonResponse(
            {
                "sum_rating": obj.likes.sum_rating(),
                "user_is_fan": user_is_fan,
                "user_is_hater": user_is_hater,
            },
            status=200,
        )
