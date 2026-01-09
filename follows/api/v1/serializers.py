from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer cho Profile API
    Returns profile với username, bio, image, following
    Logic xử lý following được thực hiện ở View
    """
    following = serializers.BooleanField(read_only=True)  # Nhận từ view

    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'following']
        read_only_fields = ['username', 'bio', 'image']
