from rest_framework import serializers

from comments.models import Comment
from follows.api.v1.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer cho Comment API
    """
    author = ProfileSerializer(source='user', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'createdAt', 'updatedAt', 'author']
        read_only_fields = ['id', 'author']

    def validate_body(self, value):
        """Validate comment body"""
        if not value or not value.strip():
            raise serializers.ValidationError("Comment body cannot be empty")

        if len(value.strip()) < 1:
            raise serializers.ValidationError("Comment body must be at least 1 character")

        return value.strip()

    def to_representation(self, instance):
        """Add following status to author"""
        data = super().to_representation(instance)

        # Add author with following status
        request = self.context.get('request')
        if request and hasattr(instance, 'user'):
            from follows.models import Follow

            # Serialize author first
            author_data = ProfileSerializer(instance.user).data

            # Then add following status
            following = False
            if request.user.is_authenticated:
                following = Follow.objects.filter(
                    user=request.user,
                    follows=instance.user
                ).exists()

            author_data['following'] = following
            data['author'] = author_data

        return data
