import re
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    STATUS_DRAFT, STATUS_PUBLISH = list(range(2))

    STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISH, 'Publish')
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


User.add_to_class("__str__", User.get_full_name)
