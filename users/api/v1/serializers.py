from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with JWT token"""
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'image', 'token', 'password']
        extra_kwargs = {
            'bio': {'required': False, 'allow_blank': True},
            'image': {'required': False, 'allow_blank': True},
        }

    def get_token(self, obj):
        """Generate JWT token for user"""
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        """Update user with proper password hashing"""
        password = validated_data.pop('password', None)

        # Update password separately using set_password
        if password:
            instance.set_password(password)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate_email(self, value):
        """Validate email uniqueness"""
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_username(self, value):
        """Validate username uniqueness"""
        user = self.instance
        if User.objects.filter(username=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError('Username already exists')
        return value
