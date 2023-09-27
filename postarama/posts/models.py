from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from pytils import translit
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

from bookmarks.models import Bookmark
from bookmarks.services import has_a_bookmark
from likes.models import Like

User = get_user_model()


class RuTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return translit.slugify(self.name)[:128]


class RuTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return RuTag


class PublishedManager(models.Manager):
    def published(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')

    def unpublished(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='draft')


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    # text = models.TextField(verbose_name='Текст')
    text = MarkdownxField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True, verbose_name='Группа',
                              related_name="posts")
    tags = TaggableManager(through=RuTaggedItem)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = GenericRelation(Like, related_query_name='posts')
    bookmarks = GenericRelation(Bookmark, related_query_name='posts')

    # objects = models.Manager()
    objects = PublishedManager()

    def in_favorites(self, user):
        return has_a_bookmark(self, user)

    def save(self, *args, **kwargs):
        self.slug = translit.slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def formatted_markdown(self):
        return markdownify(self.text)

    def get_absolute_url(self):
        return reverse('post',
                       args=[self.author.username,
                             self.id])

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    likes = GenericRelation(Like, related_query_name='comments')

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='parent_%(class)s',
                               verbose_name='parent comment'
                               )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post} - {self.text}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        unique_together = ('user', 'author')


class GroupFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='group_follower')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='followers')

    class Meta:
        unique_together = ('user', 'group')
