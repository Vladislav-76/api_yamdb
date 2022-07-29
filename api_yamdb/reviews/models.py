from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        max_length=300,
        blank=True,
    ),
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=ROLES,
        default='user'
    )
