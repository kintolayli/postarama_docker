# posts/tests/tests_url.py
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.test import TestCase, Client
from django.urls import reverse
import os

import tempfile

from posts.models import Post, Group, Follow, Comment

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username='StasBasov')
        cls.user_2 = User.objects.create_user(username='NicolayBaskov')
        cls.user_3 = User.objects.create_user(username='MarlinManson')
        cls.authorized_client = Client()
        cls.authorized_client_2 = Client()
        cls.authorized_client.force_login(cls.user_1)
        cls.authorized_client_2.force_login(cls.user_2)

        cls.unauthorized_client = Client()

        cls.test_group = Group.objects.create(title='Кошки',
                                              slug='cats',
                                              description='Посты про кошек')

        cls.key = make_template_fragment_key('index_page')

        cls.index_url = reverse('index')
        cls.group_url = reverse('group_posts',
                                kwargs={'slug': cls.test_group.slug})
        cls.new_post_url = reverse('new_post')
        cls.profile_url = reverse('profile',
                                  kwargs={'username': cls.user_1.username})

    def test_authorized_user_new_post(self):
        current_posts_count = Post.objects.count()
        response = self.authorized_client.post(self.new_post_url, {
            'text': 'Это текст публикации'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), current_posts_count + 1)

    def test_unauthorized_user_new_post(self):
        current_posts_count = Post.objects.count()
        response = self.unauthorized_client.post(self.new_post_url, {
            'text': 'Это текст публикации'}, follow=True)

        expected_url = f'{reverse("login")}?next={reverse("new_post")}'

        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        self.assertEqual(Post.objects.count(), current_posts_count)

    def test_unauthorized_user_edit_post(self):
        create_post = self.authorized_client.post(self.new_post_url, {
            'text': 'Это текст публикации'}, follow=True)
        new_post = Post.objects.get(id=1)

        edit_post_url = reverse('post_edit',
                                kwargs={'username': self.user_1.username,
                                        'post_id': new_post.id})

        edit_post = self.unauthorized_client.post(
            edit_post_url,
            {'text': 'Отредактированный текст публикации',
             },
            follow=True)

        expected_url = (
            f'{reverse("login")}?next={edit_post_url}')

        self.assertRedirects(edit_post, expected_url, status_code=302,
                             target_status_code=200)

    def test_post_is_created_everywhere(self):
        cache.clear()
        create_post = self.authorized_client.post(self.new_post_url, {
            'text': 'Это текст публикации',
            'group': self.test_group.id
        }, follow=True)

        post = Post.objects.get(id=1)

        urls = [self.index_url,
                self.profile_url, f'{self.profile_url}{post.id}/',
                self.group_url]
        self.urls_test(urls, post)

    def test_authorized_user_edit_post_and_post_changed_everywhere(self):
        cache.clear()
        new_group = Group.objects.create(title='Собаки',
                                         slug='dogs',
                                         description='Посты про собак')
        new_group_url = reverse('group_posts', kwargs={'slug': new_group.slug})

        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)

        edit_post_url = reverse('post_edit',
                                kwargs={'username': self.user_1.username,
                                        'post_id': post.id})
        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        edit_post = self.authorized_client.post(
            edit_post_url,
            {'text': 'Отредактированный текст публикации',
             'group': new_group.id
             },
            follow=True)

        post_after_edit = Post.objects.get(id=1)

        urls = [self.index_url, self.profile_url,
                post_url, new_group_url]
        self.urls_test(urls, post_after_edit.text)

        response = self.authorized_client.get(self.group_url)
        self.assertNotContains(response, post_after_edit.text)

    def test_post_with_image_is_exists(self):
        cache.clear()
        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)
        edit_post_url = reverse('post_edit',
                                kwargs={'username': self.user_1.username,
                                        'post_id': post.id})

        img = Image.new('RGBA', (20, 20), 'white')

        with tempfile.TemporaryDirectory() as tmpdirname:
            path = os.path.join(tmpdirname, 'rectangle.png')
            img.save(path)

            with open(path, 'rb') as img:
                post_with_image = self.authorized_client.post(
                    edit_post_url,
                    {
                        'author': self.user_1,
                        'text': 'post with image',
                        'image': img})


        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        response = self.authorized_client.get(post_url)

        self.assertContains(response, "<img")

    def test_post_with_image_is_exists_everywhere(self):
        cache.clear()
        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)
        edit_post_url = reverse('post_edit',
                                kwargs={'username': self.user_1.username,
                                        'post_id': post.id})

        img = Image.new('RGBA', (20, 20), 'white')

        with tempfile.TemporaryDirectory() as tmpdirname:
            path = os.path.join(tmpdirname, 'rectangle.png')
            img.save(path)

            with open(path, 'rb') as img:
                post_with_image = self.authorized_client.post(
                    edit_post_url,
                    {'author': self.user_1,
                     'text': 'post with image',
                     'image': img,
                     'group': self.test_group.id,
                     }
                )

        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        urls = [self.index_url, self.profile_url, self.group_url, post_url]
        self.urls_test(urls, "<img")

    def test_post_with_image_upload_only_image(self):
        cache.clear()
        ERROR = ('Загрузите правильное изображение. Файл, который вы '
                 'загрузили, поврежден или не является изображением.')

        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)
        edit_post_url = reverse('post_edit',
                                kwargs={'username': self.user_1.username,
                                        'post_id': post.id})

        # открываем любой файл, не изображение,
        # для проверки срабатывания защиты
        with open('templates/base.html', 'rb') as img:
            response = self.authorized_client.post(
                edit_post_url,
                {'author': self.user_1,
                 'text': 'post with image',
                 'image': img,
                 'group': self.test_group.id,
                 }
            )

        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        response_2 = self.authorized_client.get(post_url)
        self.assertNotContains(response_2, "<img")
        self.assertFormError(response, form='form', field='image',
                             errors=ERROR)

    def test_cache_is_work(self):
        response_old = self.authorized_client.get(reverse('index'))

        post = self.authorized_client.post(
            self.new_post_url,
            {'text': 'текст публикации',
             },
            follow=True)

        response_new = self.authorized_client.get(reverse('index'))
        self.assertEqual(response_old.content, response_new.content)
        cache.clear()
        response_newest = self.authorized_client.get(reverse('index'))
        self.assertNotEqual(response_old.content, response_newest.content)

    def test_follow_and_unfollow(self):
        followers_count_user_2 = Follow.objects.filter(
            user=self.user_2).count()

        follow_to_user_1 = reverse('profile_follow',
                                   kwargs={'username': self.user_1.username})
        unfollow_to_user_1 = reverse('profile_unfollow',
                                     kwargs={'username': self.user_1.username})

        self.authorized_client_2.get(follow_to_user_1)

        followers_count_user_2_after_follow = Follow.objects.filter(
            user=self.user_2).count()

        self.assertNotEqual(followers_count_user_2,
                            followers_count_user_2_after_follow)

        self.authorized_client_2.get(unfollow_to_user_1)

        followers_count_user_2_after_unfollow = Follow.objects.filter(
            user=self.user_2).count()

        self.assertEqual(followers_count_user_2,
                         followers_count_user_2_after_unfollow)

    def test_view_post_if_user_is_subscribed_to_another_users(self):
        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)

        follow_to_user_1_url = reverse('profile_follow',
                                       kwargs={
                                           'username': self.user_1.username})
        unfollow_to_user_1_url = reverse('profile_unfollow',
                                         kwargs={
                                             'username': self.user_1.username})

        follow_index_url = reverse('follow_index')

        self.authorized_client_2.get(follow_to_user_1_url)

        response = self.authorized_client_2.get(follow_index_url)
        self.assertContains(response, post.text)

        self.authorized_client_2.get(unfollow_to_user_1_url)

        response = self.authorized_client_2.get(follow_index_url)
        self.assertNotContains(response, post.text)

    def test_only_an_authorized_user_can_comment_posts(self):
        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)

        comment_url = reverse('add_comment',
                              kwargs={'username': self.user_1.username,
                                      'post_id': post.id})

        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        self.authorized_client_2.post(comment_url,
                                      {'text': 'новый комментарий',
                                       'post': post.id,
                                       'author': self.user_2},
                                      follow=True)
        comment = Comment.objects.get(id=1)

        response = self.authorized_client_2.get(post_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment.text)

    def test_authorized_user_can_comment_delete(self):
        post = Post.objects.create(author=self.user_1,
                                   text='Это текст публикации',
                                   group=self.test_group)

        comment_url = reverse('add_comment',
                              kwargs={'username': self.user_1.username,
                                      'post_id': post.id})

        post_url = reverse('post',
                           kwargs={'username': self.user_1.username,
                                   'post_id': post.id})

        self.authorized_client_2.post(comment_url,
                                      {'text': 'новый комментарий',
                                       'post': post.id,
                                       'author': self.user_2},
                                      follow=True)
        self.authorized_client_2.post(comment_url,
                                      {'text': 'еще один комментарий',
                                       'post': post.id,
                                       'author': self.user_2},
                                      follow=True)

        comments_count_before_delete = Comment.objects.count()
        comment = Comment.objects.get(id=1)
        comment.delete()
        comments_count_after_delete = Comment.objects.count()

        self.assertNotEqual(comments_count_before_delete,
                            comments_count_after_delete)

    def urls_test(self, urls: list, arg):
        for url in urls:
            response_1 = self.authorized_client.get(url)
            response_2 = self.unauthorized_client.get(url)
            self.assertContains(response_1, arg)
            self.assertContains(response_2, arg)
