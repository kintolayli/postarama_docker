from bookmarks import views
from django.urls import path

urlpatterns = [
    # #  Добавление или удаление закладки
    # path('<str:username>/<int:post_id>/add-or-remove-bookmark/',
    #      views.add_or_remove_bookmark,
    #      name='add_or_remove_bookmark'),

    #  Добавление или удаление закладки view как класс
    path('<str:username>/<int:post_id>/bookmark/',
         views.BookmarkAddOrRemove.as_view(),
         name='bookmark'),
]
