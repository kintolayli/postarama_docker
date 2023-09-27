import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from bookmarks.services import add_bookmark, remove_bookmark, has_a_bookmark
from posts.models import Post

User = get_user_model()


class BookmarkAddOrRemove(View):
    def post(self, request, username, post_id):
        post = get_object_or_404(Post, author__username=username, pk=post_id)
        user = request.user
        if has_a_bookmark(post, user):
            remove_bookmark(post, user)
            bookmark = True
        else:
            add_bookmark(post, user)
            bookmark = False

        return JsonResponse({"bookmark": bookmark,
                             "count": post.bookmarks.count()
                             }, status=200)

