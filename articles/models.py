from django.db import models

from core.constants import MAX_LENGTH_SHORT, MAX_LENGTH_MEDIUM, MAX_LENGTH_DESCRIPTION
from core.models import TimestampedModel


class Article(TimestampedModel):
    slug = models.CharField(max_length=MAX_LENGTH_SHORT)
    title = models.CharField(max_length=MAX_LENGTH_MEDIUM)
    description = models.CharField(max_length=MAX_LENGTH_DESCRIPTION)
    body = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='articles')

    class Meta:
        db_table = 'articles'
        ordering = ['created_at']

    def __str__(self):
        return self.title
