from django.db import models
from django.conf import settings

from core.models import TimestampedModel


class Follow(TimestampedModel):
    """
    Follow model để quản lý quan hệ follow giữa users
    user follows another_user
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'  # user.following.all() -> danh sách người mà user đang follow
    )
    follows = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'  # user.followers.all() -> danh sách người đang follow user này
    )

    class Meta:
        db_table = 'follows'
        ordering = ['created_at']
        # Đảm bảo một user chỉ follow một user khác duy nhất 1 lần
        unique_together = ('user', 'follows')
        indexes = [
            models.Index(fields=['user', 'follows']),
        ]

    def __str__(self):
        return f'{self.user.username} follows {self.follows.username}'
