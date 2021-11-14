import uuid

from django.utils import timezone
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, default='')
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, db_index=True,
                            unique=True, allow_unicode=True, default=uuid.uuid1)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #   shop:product_in_category
        return reverse('blog:blog_in_category', args=[self.slug])


class HashTag(models.Model):
    hashtag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.hashtag_name


class Blog(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='blogs')  # products

    slug = slug = models.SlugField(
        max_length=50, db_index=True, unique=True, allow_unicode=True, default=uuid.uuid1)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    body = models.TextField()
    hashtag = models.ManyToManyField(HashTag)

    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='bookmark'
    )

    class Meta:
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def get_absolute_url(self):
        reverse('blog:detail', args=[self.id, self.slug])
        # shop:product_detail


class Comment(models.Model):
    post = models.ForeignKey(
        Blog, related_name='comments', on_delete=models.CASCADE)
    author_name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    comment_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = slug = models.SlugField(
        max_length=50, db_index=True, unique=True, allow_unicode=True, default=uuid.uuid1)

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        reverse('blog:detail', args=[self.id, self.slug])
