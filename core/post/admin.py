from django.contrib import admin

from .models import Post, PostReaction, PostSeen


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_posted')
    search_fields = ('title',)
    list_select_related = ('author', )
    ordering = ('date_posted',)
    list_per_page = 20
    list_max_show_all = 100

    fieldsets = (
        (None, {'fields': ('author', 'title', 'description', 'tags')}),
    )


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'reaction_type')
    list_select_related = ('author', 'post')
    ordering = ('created_at',)
    list_per_page = 20
    list_max_show_all = 100

    fieldsets = (
        (None, {'fields': ('author', 'post', 'reaction_type')}),
    )


@admin.register(PostSeen)
class PostSeenAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'seen_at')
    list_select_related = ('post', 'user')
    ordering = ('seen_at',)
    list_per_page = 20
    list_max_show_all = 100

    fieldsets = (
        (None, {'fields': ('post', 'user', 'seen_at')}),
    )

