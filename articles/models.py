from django.db import models
from django.utils.text import slugify

from core.constants import MAX_LENGTH_SHORT, MAX_LENGTH_MEDIUM, MAX_LENGTH_DESCRIPTION
from core.models import TimestampedModel


class Article(TimestampedModel):
    slug = models.SlugField(max_length=MAX_LENGTH_SHORT, unique=True)
    title = models.CharField(max_length=MAX_LENGTH_MEDIUM)
    description = models.CharField(max_length=MAX_LENGTH_DESCRIPTION)
    body = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField('tags.Tag', related_name='articles', blank=True)
    favorited_by = models.ManyToManyField('users.User', related_name='favorited_articles', blank=True)

    class Meta:
        db_table = 'articles'
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
