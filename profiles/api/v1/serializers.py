from rest_framework import serializers

from users.models import User
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer cho Profile API
    Returns profile với username, bio, image, following
    """
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'following']

    def get_following(self, obj):
        """
        Kiểm tra xem current user có đang follow user này không
        """
        request = self.context.get('request')

        # Nếu không có request hoặc user chưa authenticated -> following = False
        if not request or not request.user.is_authenticated:
            return False

        # Kiểm tra xem current user có follow user này không
        return Profile.objects.filter(
            user=request.user,
            follows=obj
        ).exists()
