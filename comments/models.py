from django.db import models
from django.core.validators import MinLengthValidator

from core.models import TimestampedModel


class Comment(TimestampedModel):
    body = models.TextField(
        blank=False,
        validators=[MinLengthValidator(1, message="Comment body cannot be empty")]
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.email} on {self.article.title}"
