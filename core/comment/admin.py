from django.contrib import admin

from .models import Comment, CommentReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_answered', 'is_correct')
    list_editable = ('is_correct',)
    list_select_related = ('author', 'post')
    ordering = ('date_answered',)
    list_per_page = 20
    list_max_show_all = 100
    
    fieldsets = (
        (None, {'fields': ('author', 'post', 'content')}),
    )
    

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'reaction_type')
    list_select_related = ('author', 'comment')
    ordering = ('created_at',)
    list_per_page = 20
    list_max_show_all = 100

    fieldsets = (
        (None, {'fields': ('author', 'comment', 'reaction_type')}),
    )



