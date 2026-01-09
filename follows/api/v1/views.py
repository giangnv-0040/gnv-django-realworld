from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from users.models import User
from follows.models import Follow
from follows.api.v1.serializers import ProfileSerializer


class GetProfileView(APIView):
    """
    GET /api/profiles/:username
    Get a user profile
    """
    permission_classes = [AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        # Logic kiểm tra following ở đây
        following = False
        if request.user.is_authenticated:
            following = Follow.objects.filter(
                user=request.user,
                follows=user
            ).exists()

        # Serialize user data và thêm following
        serializer = ProfileSerializer(user)
        profile_data = serializer.data
        profile_data['following'] = following

        return Response({'profile': profile_data})


class FollowUserView(APIView):
    """
    POST /api/profiles/:username/follow - Follow user
    DELETE /api/profiles/:username/follow - Unfollow user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        """Follow user"""
        user_to_follow = get_object_or_404(User, username=username)

        # Không thể follow chính mình
        if request.user == user_to_follow:
            return Response(
                {'errors': {'body': ['Cannot follow yourself']}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tạo relationship follow
        Follow.objects.get_or_create(user=request.user, follows=user_to_follow)

        # Serialize và set following = True
        serializer = ProfileSerializer(user_to_follow)
        profile_data = serializer.data
        profile_data['following'] = True

        return Response({'profile': profile_data})

    def delete(self, request, username):
        """Unfollow user"""
        user_to_unfollow = get_object_or_404(User, username=username)

        # Xóa relationship follow
        Follow.objects.filter(user=request.user, follows=user_to_unfollow).delete()

        # Serialize và set following = False
        serializer = ProfileSerializer(user_to_unfollow)
        profile_data = serializer.data
        profile_data['following'] = False

        return Response({'profile': profile_data})
