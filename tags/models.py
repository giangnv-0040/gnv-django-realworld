from django.db import models

from core.constants import MAX_LENGTH_SHORT
from core.models import TimestampedModel


class Tag(TimestampedModel):
    name = models.CharField(max_length=MAX_LENGTH_SHORT, blank=True, default="")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tags')

    class Meta:
        db_table = 'tags'
        ordering = ['created_at']

    def __str__(self):
        return self.name
