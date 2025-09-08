from django.contrib import admin
from .models import BlogPost, UserProfile, Bookmark, BlogImage, Vote, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'votes')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'created_at')
    search_fields = ('user__username', 'bio')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'user')

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'caption', 'order')
    list_filter = ('post',)
    ordering = ('post', 'order')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_life', 'created_at')
    list_filter = ('is_life', 'created_at', 'user')
    search_fields = ('user__username', 'post__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'parent')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
