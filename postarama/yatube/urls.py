from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from markdownx import urls as markdownx


handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("feedback.urls")),
    path("", include("posts.urls")),
    path("", include("likes.urls")),
    path("", include("bookmarks.urls")),
    path('about/', include('about.urls', namespace='about')),
]


urlpatterns += [url(r"^markdownx/", include(markdownx))]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
        url(
            r"^static/(?P<path>.*)$",
            serve,
            {"document_root": settings.STATIC_ROOT},
        ),
    ]
