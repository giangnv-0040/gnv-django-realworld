from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from tags.models import Tag
from tags.api.v1.serializers import TagSerializer


class TagsView(APIView):
    """
    GET /api/tags - Get all tags (no authentication required)
    POST /api/tags - Create new tag (authentication required)
    """

    def get_permissions(self):
        """
        GET: AllowAny
        POST: IsAuthenticated
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """
        Lấy danh sách tất cả các tags
        Trả về array of tag names
        """
        # Lấy tất cả tags, distinct by name
        tags = Tag.objects.values_list('name', flat=True).distinct()

        return Response({
            'tags': list(tags)
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Tạo tag mới
        """
        # Get tag data from request
        tag_data = request.data.get('tag', {})

        # Validate and create tag using serializer
        serializer = TagSerializer(data=tag_data, context={'request': request})

        if serializer.is_valid():
            tag = serializer.save()
            return Response({
                'tag': {'name': tag.name}
            }, status=status.HTTP_201_CREATED)

        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
