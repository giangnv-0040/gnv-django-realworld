from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import MAX_LENGTH_SHORT, MAX_LENGTH_LONG
from core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    email = models.EmailField(unique=True, blank=False)

    token = models.CharField(max_length=MAX_LENGTH_LONG, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    image = models.URLField(max_length=MAX_LENGTH_LONG, blank=True, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['created_at']
        db_table = 'users'

    def __str__(self):
        return self.email
