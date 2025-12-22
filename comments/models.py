from django.db import models

from core.constants import MAX_LENGTH_DESCRIPTION
from core.models import TimestampedModel


class Comment(TimestampedModel):
    body = models.CharField(max_length=MAX_LENGTH_DESCRIPTION, blank=True, default="")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.email} on {self.article.title}"
