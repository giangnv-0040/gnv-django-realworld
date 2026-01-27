import django_filters
from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    """
    Filter backend for Article list API

    Query parameters:
    - tag: Filter by tag name
    - author: Filter by author username
    - favorited: Filter by username who favorited the article
    """
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    favorited = django_filters.CharFilter(field_name='favorited_by__username', lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['tag', 'author', 'favorited']
