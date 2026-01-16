from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer cho Tag API
    """
    name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Tag
        fields = ['name']

    def validate_name(self, value):
        """
        Validate tag name
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Tag name cannot be empty")

        # Check if tag already exists
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError("Tag already exists")

        return value.strip()

    def create(self, validated_data):
        """
        Create new tag
        """
        # Get user from context
        user = self.context['request'].user

        tag = Tag.objects.create(
            name=validated_data['name'],
            user=user
        )
        return tag
