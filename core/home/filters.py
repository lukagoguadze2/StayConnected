import django_filters
from django.db import models

from post.models import Post

class PostFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='filter_by_title_and_description', 
        label='Search by text'
    )
    tag = django_filters.NumberFilter(
        field_name="tags__id", 
        lookup_expr="exact", 
        label="Filter by Tag ID"
    )

    class Meta:
        model = Post
        fields = ['query', 'tag']

    def filter_by_title_and_description(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) | 
            models.Q(description__icontains=value)
        )
