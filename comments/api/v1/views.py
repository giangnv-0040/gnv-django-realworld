from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from comments.models import Comment
from comments.api.v1.serializers import CommentSerializer
from articles.models import Article


class CommentsView(generics.ListCreateAPIView):
    """
    GET /api/articles/:slug/comments - Get comments for article
    POST /api/articles/:slug/comments - Add comment to article
    """
    serializer_class = CommentSerializer

    def get_permissions(self):
        """GET: AllowAny, POST: IsAuthenticated"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Get comments for specific article"""
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return Comment.objects.filter(article=article).select_related('user').order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Custom list response format"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'comments': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """Create comment for article"""
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)

        comment_data = request.data.get('comment', {})

        serializer = self.get_serializer(data=comment_data)
        serializer.is_valid(raise_exception=True)

        # Save with user and article
        comment = serializer.save(user=request.user, article=article)

        return Response({
            'comment': self.get_serializer(comment).data
        }, status=status.HTTP_201_CREATED)


class CommentDetailView(generics.DestroyAPIView):
    """
    DELETE /api/articles/:slug/comments/:id - Delete comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """Filter by article slug"""
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return Comment.objects.filter(article=article)

    def destroy(self, request, *args, **kwargs):
        """Delete comment with author check"""
        comment = self.get_object()

        # Check if user is the comment author
        if comment.user != request.user:
            return Response({
                'errors': {'comment': ['You are not the author of this comment']}
            }, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
