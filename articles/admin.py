from django.contrib import admin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    exclude = ('like_users',)
    list_display = ('category', 'title', 'content', 'user')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
