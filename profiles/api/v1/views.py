from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from users.models import User
from profiles.api.v1.serializers import ProfileSerializer


class GetProfileView(APIView):
    """
    GET /api/profiles/:username

    Authentication optional, returns a Profile
    """
    permission_classes = [AllowAny]

    def get(self, request, username):
        """
        Lấy thông tin profile của user theo username
        """
        user = get_object_or_404(User, username=username)

        serializer = ProfileSerializer(user, context={'request': request})

        return Response({
            'profile': serializer.data
        }, status=status.HTTP_200_OK)
