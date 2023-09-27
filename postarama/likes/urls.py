from django.urls import path

from likes import views
from likes.models import Like

urlpatterns = [
    #  Повышение рейтинга публикации view в виде класса
    path('<str:username>/<int:post_id>/like/',
         views.PostRatingUpDown.as_view(vote_type=Like.LIKE),
         name='post_like'),

    #  Понижение рейтинга публикации view в виде класса
    path('<str:username>/<int:post_id>/dislike/',
         views.PostRatingUpDown.as_view(vote_type=Like.DISLIKE),
         name='post_dislike'),

    #  Повышение рейтинга комментария view в виде класса
    path('<str:username>/<int:post_id>/comment/<int:comment_id>/like/',
         views.CommentRatingUpDown.as_view(vote_type=Like.LIKE),
         name='comment_like'),

    #  Понижение рейтинга комментария view в виде класса
    path('<str:username>/<int:post_id>/comment/<int:comment_id>/dislike/',
         views.CommentRatingUpDown.as_view(vote_type=Like.DISLIKE),
         name='comment_dislike'),
]
