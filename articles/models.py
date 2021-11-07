from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Article(models.Model):
    CAT_WORK = 'wk'
    CAT_LIFE = 'lf'
    CAT_FINANCE = 'fn'
    CAT_QUESTION = 'qt'
    CATEGORY_CHOICES = [
        (CAT_WORK, '근무 이야기'),
        (CAT_LIFE, '일상 이야기'),
        (CAT_FINANCE, '머니 이야기'),
        (CAT_QUESTION, '질문 이야기'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    title = models.CharField(max_length=30)
    content = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=CAT_WORK)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
