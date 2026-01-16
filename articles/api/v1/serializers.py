from rest_framework import serializers

from articles.models import Article
from users.models import User
from follows.api.v1.serializers import ProfileSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer cho Article API
    """
    author = ProfileSerializer(read_only=True)
    tagList = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body',
            'tagList', 'createdAt', 'updatedAt',
            'favorited', 'favoritesCount', 'author'
        ]
        read_only_fields = ['slug', 'author']

    def validate_title(self, value):
        """Validate title"""
        from django.utils.text import slugify

        # Check uniqueness based on slug
        slug = slugify(value)

        # Nếu đang create (không có instance)
        if not self.instance:
            if Article.objects.filter(slug=slug).exists():
                raise serializers.ValidationError("Article with this title already exists")
        # Nếu đang update và đổi title
        elif self.instance and self.instance.slug != slug:
            if Article.objects.filter(slug=slug).exists():
                raise serializers.ValidationError("Article with this title already exists")

        return value.strip()

    def validate_tagList(self, value):
        """Validate tagList"""
        if not value:
            return value

        # Check max tags
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 tags allowed")

        # Check and clean tags
        cleaned_tags = []
        for tag in value:
            tag_cleaned = tag.strip()
            if not tag_cleaned:
                raise serializers.ValidationError("Tag name cannot be empty")
            if len(tag_cleaned) > 50:
                raise serializers.ValidationError("Tag name too long (max 50 characters)")
            cleaned_tags.append(tag_cleaned.lower())  # Lowercase for consistency

        # Check duplicate tags
        if len(cleaned_tags) != len(set(cleaned_tags)):
            raise serializers.ValidationError("Duplicate tags are not allowed")

        return cleaned_tags

    def validate(self, data):
        """Cross-field validation"""
        # Check if title and body are identical
        if 'title' in data and 'body' in data:
            if data['title'].lower() == data['body'].lower():
                raise serializers.ValidationError(
                    "Title and body cannot be identical"
                )

        return data

    def get_favorited(self, obj):
        """Check if current user favorited this article"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.favorited_by.filter(id=request.user.id).exists()

    def get_favoritesCount(self, obj):
        """Get number of users who favorited this article"""
        return obj.favorited_by.count()

    def create(self, validated_data):
        """Create article with tags"""
        tag_names = validated_data.pop('tagList', [])
        author = self.context['request'].user

        article = Article.objects.create(author=author, **validated_data)

        # Add tags
        if tag_names:
            from tags.models import Tag
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name, defaults={'user': author})
                article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        """Update article"""
        tag_names = validated_data.pop('tagList', None)

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update tags if provided
        if tag_names is not None:
            from tags.models import Tag
            instance.tags.clear()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'user': instance.author}
                )
                instance.tags.add(tag)

        return instance

    def to_representation(self, instance):
        """Custom representation to add tagList and author with following status"""
        data = super().to_representation(instance)

        # Add tagList from ManyToMany relationship
        data['tagList'] = list(instance.tags.values_list('name', flat=True))

        # Add author with following status
        request = self.context.get('request')
        if request and hasattr(instance, 'author'):
            from follows.models import Follow

            # Serialize author first
            author_data = ProfileSerializer(instance.author).data

            # Then add following status
            following = False
            if request.user.is_authenticated:
                following = Follow.objects.filter(
                    user=request.user,
                    follows=instance.author
                ).exists()

            author_data['following'] = following
            data['author'] = author_data

        return data
