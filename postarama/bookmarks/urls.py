from bookmarks import views
from django.urls import path

urlpatterns = [
    #  Добавление или удаление закладки view как класс
    path(
        "<str:username>/<int:post_id>/bookmark/",
        views.BookmarkAddOrRemove.as_view(),
        name="bookmark",
    ),
]
