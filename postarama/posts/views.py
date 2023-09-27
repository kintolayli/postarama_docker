import datetime as dt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (SearchVector, SearchQuery,
                                            SearchRank)
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404, redirect
from likes import services
from likes.models import Like
from posts.forms import PostForm, CommentForm, SearchForm
from posts.models import Post, Group, Comment, Follow, GroupFollow
from taggit.models import Tag

User = get_user_model()

PAGINATOR_PAGE_COUNT = 10

FOLLOW_SUCCESS_USER = ('Готово! Теперь ты будешь получать обновления '
                       'от этого пользователя.')
FOLLOW_SUCCESS_GROUP = ('Готово! Теперь ты будешь получать обновления '
                        'от этой группы.')
UNFOLLOW_SUCCESS_USER = 'Вы отписались от этого пользователя'
UNFOLLOW_SUCCESS_GROUP = 'Вы отписались от этой группы'


# @cache_page(0)
def index(request, tag_slug=None):
    #  Сортировка по количесту лайков

    # posts = Post.objects.published().annotate(
    #     posts_most_likes=Sum('likes__vote')).order_by(
    #     'posts_most_likes').select_related('author')

    posts = Post.objects.published().order_by(
        '-publish').select_related('author')

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html', {'page': page, 'paginator': paginator, 'index': True,
                       'tag': tag})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    #  Сортировка по количесту лайков

    # posts = Post.objects.published().filter(group=group).annotate(
    #     posts_most_likes=Sum('likes__vote')).order_by(
    #     'posts_most_likes').select_related('group')

    posts = Post.objects.published().filter(group=group).order_by(
        '-publish').select_related('author')

    try:
        group_follower = get_object_or_404(GroupFollow, user=request.user,
                                           group=group)
    except:
        group_follower = False

    paginator = Paginator(posts, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        "group.html",
        {'group': group, 'page': page, 'paginator': paginator,
         'group_follower': group_follower, }, )


@login_required
def posts_unpublished(request):
    posts = Post.objects.unpublished().filter(author=request.user).order_by(
        '-updated').select_related('author')

    paginator = Paginator(posts, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html', {'page': page, 'paginator': paginator})


@login_required
def posts_in_bookmarks(request):
    posts = Post.objects.published().filter(
        bookmarks__user=request.user).order_by(
        '-updated').select_related('author')

    paginator = Paginator(posts, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html', {'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)

    context = {
        "form": form,
        "edit": False,
    }

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            form.save_m2m()

            return redirect("posts_unpublished")

        else:
            return render(request, "new_post.html", context)

    return render(request, "new_post.html", context)


def year(request):
    now = dt.datetime.today()
    return {
        'year': now.year
    }


# @cache_page(0)
def profile(request, username):
    user = get_object_or_404(User, username=username)

    posts = Post.objects.published().filter(
        author__username=username).annotate(
        posts_most_likes=Sum('likes__vote')).order_by(
        '-created').select_related('author')

    paginator = Paginator(posts, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    try:
        following = get_object_or_404(Follow, user=request.user,
                                      author__username=username)
    except Exception as e:
        following = False

    context = {
        'page': page,
        'paginator': paginator,
        'username': username,
        'posts': posts,
        'profile': user,
        'following': following
    }

    return render(request, 'profile.html', context)


# @cache_page(0)
def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)

    its_have_like = services.is_fan(post, request.user, Like.LIKE)
    its_have_dislike = services.is_fan(post, request.user, Like.DISLIKE)

    form = CommentForm(request.POST or None)

    comments = post.comments.filter(active=True).annotate(
        comments_most_likes=Sum('likes__vote')).order_by(
        'comments_most_likes').select_related('author')

    try:
        following = get_object_or_404(Follow, user=request.user,
                                      author__username=username)
    except Exception as e:
        following = False

    #  Список похожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.published().filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'form': form,
        'username': username,
        'post': post,
        'profile': post.author,
        'comments': comments,
        'following': following,
        'post_view': True,
        'similar_posts': similar_posts,
        'its_have_like': its_have_like,
        'its_have_dislike': its_have_dislike
    }

    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    context = {
        "form": form,
        'post': post,
        "edit": True,
    }

    if request.user == post.author:
        if request.method == 'POST':

            context["form"] = form

            if form.is_valid():
                form.save()

                return redirect('post', username, post_id)
            else:
                return render(request, "new_post.html", context)
        else:
            return render(request, "new_post.html", context)
    else:
        return redirect('post', username, post_id)


@login_required
def post_delete(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)

    if request.user == post.author:
        post.delete()
        return redirect('index')


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)

    context = {
        "form": form,
        "profile": request.user,
        "post": post,
        "edit": False,
    }

    if request.method == 'POST':
        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post', username, post_id)

        else:
            return render(request, "post.html", context)
    else:
        return render(request, "post.html", context)


@login_required
def edit_comment(request, username, post_id, comment_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    comment = get_object_or_404(Comment, author=request.user,
                                post=post_id, pk=comment_id)

    form = CommentForm(request.POST or None, instance=comment)
    # comments = Comment.objects.filter(
    #     post=post).order_by("-created").select_related('post')

    context = {
        'form': form,
        'username': username,
        'post': post,
        'profile': post.author,
        "comment": comment,
        "edit": True,

        # 'comments': comments,
    }

    if comment.author == request.user:
        if request.method == 'POST':
            if form.is_valid():
                comment.save()

                return redirect('post', username, post_id)
            else:
                return render(request, "post.html", context)
        else:
            return render(request, "post.html", context)
    else:
        return render(request, "post.html", context)


def delete_comment(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, author=request.user,
                                post=post_id, pk=comment_id)

    if request.user == comment.author:
        comment.delete()

    return redirect('post', username, post_id)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользовательской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    #  Сортировка по количеству лайков

    # selected_authors_list = Post.objects.published().filter(
    #     author__following__user=request.user).annotate(
    #     posts_most_likes=Sum('likes__vote')).order_by(
    #     'posts_most_likes').select_related('author')

    author_posts_list = Post.objects.published().filter(
        author__following__user=request.user).select_related('author')

    group_posts_list = Post.objects.published().filter(
        group__followers__user=request.user).select_related('author')

    result_list = author_posts_list.union(
        group_posts_list, all=False).order_by('-publish')

    paginator = Paginator(result_list, PAGINATOR_PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html", {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)

    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
        messages.success(request, FOLLOW_SUCCESS_USER)

    return redirect('profile', username)


@login_required
def group_follow(request, slug):
    group = get_object_or_404(Group, slug=slug)

    GroupFollow.objects.get_or_create(user=request.user, group=group)
    messages.success(request, FOLLOW_SUCCESS_GROUP)

    return redirect('group_posts', slug)


@login_required
def profile_unfollow(request, username):
    if request.user.username != username:
        subscription = get_object_or_404(Follow, user=request.user,
                                         author__username=username)
        subscription.delete()

        messages.success(request, UNFOLLOW_SUCCESS_USER)

    return redirect('profile', username)


@login_required
def group_unfollow(request, slug):
    group = get_object_or_404(Group, slug=slug)
    subscription = get_object_or_404(GroupFollow, user=request.user,
                                     group=group)
    subscription.delete()
    messages.success(request, UNFOLLOW_SUCCESS_GROUP)

    return redirect('group_posts', slug)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:

        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # trigram similarity

            # results = Post.objects.published().annotate(
            #     similarity=TrigramSimilarity('text', query),
            # ).filter(similarity__gt=0.1).order_by('-similarity')

            search_vector = SearchVector('title', 'text')
            search_query = SearchQuery(query)
            results = Post.objects.published().annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)).filter(
                search=search_query).order_by('-rank')

            # search_vector = SearchVector(
            #     'title', weight='A') + SearchVector('text', weight='B')
            # search_query = SearchQuery(query)
            # results = Post.objects.published().annotate(
            #     rank=SearchRank(search_vector, search_query)).filter(
            #     rank__gte=0.3).order_by('-rank')

    context = {
        'form': form,
        'query': query,
        'results': results,
    }

    return render(request, 'search.html', context)
