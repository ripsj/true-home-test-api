import django_filters
from django_filters import rest_framework as filters
from project.apps.posts.models import Posts

class TagFilter(filters.FilterSet):
    tags__tag = django_filters.CharFilter(
        field_name='tags',
        lookup_expr='tag'
    )

    class Meta:
        model = Posts
        fields = ['tags__tag',]