from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'is_published', 'view_count')
    list_filter = ('created_at', 'title')
    search_fields = ('title', 'content')


