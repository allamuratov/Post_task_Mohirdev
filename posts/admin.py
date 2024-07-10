from django.contrib import admin

from posts.models import Post, Category, Comment


# Register your models here.
@admin.register(Post)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_time', 'status']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['post', 'comment', 'author']