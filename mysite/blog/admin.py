from django.contrib import admin
from blog.models import Post, Comment
# Register your models here.
# admin.site.register(models.Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created', 'status')
    list_filter = ('title', 'author', 'publish', 'created', 'status')
    search_fields = ('title', 'body', 'author')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('publish', 'status')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active')
    list_filter = ('name', 'active')
    search_fields = ('name', 'email', 'body')

