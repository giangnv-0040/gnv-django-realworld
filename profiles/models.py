from django.db import models
from django.conf import settings

from core.models import TimestampedModel


class Profile(TimestampedModel):
    """
    Profile model để quản lý quan hệ following giữa users
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    follows = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        db_table = 'profiles'
        ordering = ['created_at']
        # Đảm bảo một user chỉ follow một user khác duy nhất 1 lần
        unique_together = ('user', 'follows')

    def __str__(self):
        return f'{self.user.username} follows {self.follows.username}'
