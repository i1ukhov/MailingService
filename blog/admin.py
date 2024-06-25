from django.contrib import admin
from blog.models import Article


@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'views_count')
    list_filter = ('title', 'views_count')
    search_fields = ('title', 'content')
