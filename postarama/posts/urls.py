from django.urls import path

from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # Главная страница с записями по тегам
    path('tag/<slug:tag_slug>/', views.index, name='index_by_tag'),
    # Страница просмотра групп
    path('group/<slug:slug>/', views.group_posts, name="group_posts"),

    # Страница поиска
    path('search/', views.post_search, name='post_search'),

    #  Добавление поста
    path('new/', views.new_post, name="new_post"),
    #  Просмотр поста
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    #  Редактирование поста
    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    #  Удаление поста
    path('<str:username>/<int:post_id>/delete/', views.post_delete,
         name='post_delete'),
    # Неопубликованные посты
    path('unpublished/', views.posts_unpublished, name="posts_unpublished"),

    #  Лента пользователя
    path("follow/", views.follow_index, name="follow_index"),
    #  Лента пользователя
    path("bookmarks/", views.posts_in_bookmarks, name="posts_in_bookmarks"),
    #  Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),

    #  Добавление комментария
    path("<username>/<int:post_id>/comment/",
         views.add_comment, name="add_comment"),
    #  Редактирование комментария
    path("<username>/<int:post_id>/comment/<int:comment_id>/edit/",
         views.edit_comment, name="edit_comment"),
    #  Удаление комментария
    path("<username>/<int:post_id>/comment/<int:comment_id>/delete/",
         views.delete_comment, name="delete_comment"),

    #  Подписаться на пользователя
    path("<str:username>/follow/",
         views.profile_follow, name="profile_follow"),
    #  Отписаться от пользователя
    path("<str:username>/unfollow/",
         views.profile_unfollow, name="profile_unfollow"),
    #  Подписаться на группу
    path("group/<slug:slug>/follow/",
         views.group_follow, name="group_follow"),
    #  Отписаться от группы
    path("group/<slug:slug>/unfollow/",
         views.group_unfollow, name="group_unfollow"),

    # path('404/', views.page_not_found, name='page_not_found'),
    # path('500/', views.server_error, name='server_error'),

]
