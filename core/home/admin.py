from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['title']
    list_per_page = 20
    list_max_show_all = 100
