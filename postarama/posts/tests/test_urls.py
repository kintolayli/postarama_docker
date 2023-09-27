# posts/tests/tests_url.py

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()

        cls.test_group = Group.objects.create(title='Кошки',
                                              slug='cats',
                                              description='Посты про кошек')

        cls.index_url = reverse('index')
        cls.group_url = reverse('group_posts',
                                kwargs={'slug': cls.test_group.slug})
        cls.new_post_url = reverse('new_post')
        cls.profile_url = reverse('profile',
                                  kwargs={'username': cls.user.username})

    def test_homepage(self):
        response = self.unauthorized_client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

    def test_force_login(self):
        response = self.authorized_client.get(self.new_post_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_newpage(self):
        response = self.unauthorized_client.get(self.new_post_url)
        expected_url = '/auth/login/?next=/new/'
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)

    def test_create_personal_profile_page(self):
        response = self.authorized_client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_page_not_found(self):
        response = self.authorized_client.get('/page_not_exists/')
        self.assertEqual(response.status_code, 404)
