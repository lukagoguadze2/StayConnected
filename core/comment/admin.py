from django.contrib import admin
from .models import Comment, CommentReaction

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post','date_answered',)
    search_fields = ('author', 'post')
    ordering = ('date_answered',)
    list_per_page = 20
    list_max_show_all = 100
    
    fieldsets = (
        (None, {'fields': ('author', 'post', 'content')}),
        ('Important dates', {'fields': ('created_at',)}),
    )
    

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    pass
