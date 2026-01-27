from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from articles.models import Article
from articles.api.v1.serializers import ArticleSerializer
from articles.api.v1.filters import ArticleFilter


class ArticlesPagination(LimitOffsetPagination):
    """Custom pagination for articles"""
    default_limit = 20
    max_limit = 100


class ArticlesView(generics.ListCreateAPIView):
    """
    GET /api/articles - List articles with filters
    POST /api/articles - Create article

    Query parameters for GET:
    - tag: Filter by tag name
    - author: Filter by author username
    - favorited: Filter by username who favorited
    - limit: Number of articles (default: 20, max: 100)
    - offset: Number of articles to skip (default: 0)
    """
    queryset = Article.objects.all().select_related('author').prefetch_related('tags', 'favorited_by')
    serializer_class = ArticleSerializer
    pagination_class = ArticlesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    def get_permissions(self):
        """GET: AllowAny, POST: IsAuthenticated"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Get base queryset with optimizations"""
        return super().get_queryset().distinct().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Custom list response format with pagination"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'articles': serializer.data,
                'articlesCount': queryset.count()
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'articles': serializer.data,
            'articlesCount': queryset.count()
        })

    def create(self, request, *args, **kwargs):
        """Custom create response format"""
        article_data = request.data.get('article', {})

        serializer = self.get_serializer(data=article_data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        return Response({
            'article': self.get_serializer(article).data
        }, status=status.HTTP_201_CREATED)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/articles/:slug - Get article
    PUT /api/articles/:slug - Update article
    DELETE /api/articles/:slug - Delete article
    """
    queryset = Article.objects.all().select_related('author').prefetch_related('tags', 'favorited_by')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        """GET: AllowAny, PUT/DELETE: IsAuthenticated"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        """Custom retrieve response format"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({'article': serializer.data})

    def update(self, request, *args, **kwargs):
        """Custom update with author check"""
        instance = self.get_object()

        # Check if user is the author
        if instance.author != request.user:
            return Response({
                'errors': {'article': ['You are not the author of this article']}
            }, status=status.HTTP_403_FORBIDDEN)

        article_data = request.data.get('article', {})

        serializer = self.get_serializer(instance, data=article_data, partial=True)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        return Response({
            'article': self.get_serializer(article).data
        })

    def destroy(self, request, *args, **kwargs):
        """Custom delete with author check"""
        instance = self.get_object()

        # Check if user is the author
        if instance.author != request.user:
            return Response({
                'errors': {'article': ['You are not the author of this article']}
            }, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteArticleView(generics.GenericAPIView):
    """
    POST /api/articles/:slug/favorite - Favorite article
    DELETE /api/articles/:slug/favorite - Unfavorite article
    """
    queryset = Article.objects.all().select_related('author').prefetch_related('tags', 'favorited_by')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def post(self, request, slug):
        """Favorite article"""
        article = self.get_object()

        # Check if already favorited
        if article.favorited_by.filter(id=request.user.id).exists():
            return Response({
                'errors': {'article': ['Article already favorited']}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Add current user to favorited_by
        article.favorited_by.add(request.user)

        serializer = self.get_serializer(article)
        return Response({'article': serializer.data})

    def delete(self, request, slug):
        """Unfavorite article"""
        article = self.get_object()

        # Check if not favorited yet
        if not article.favorited_by.filter(id=request.user.id).exists():
            return Response({
                'errors': {'article': ['Article not favorited yet']}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Remove current user from favorited_by
        article.favorited_by.remove(request.user)

        serializer = self.get_serializer(article)
        return Response({'article': serializer.data})
