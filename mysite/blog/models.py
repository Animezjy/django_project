from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 文章表
class Post(models.Model):
    STATUS_CHOICE = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=50, verbose_name="文章标题")
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="作者")
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='draft', verbose_name="文章状态")
    body = models.TextField(verbose_name="文章内容")

    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ("-publish")

    def __str__(self):
        return self.title
