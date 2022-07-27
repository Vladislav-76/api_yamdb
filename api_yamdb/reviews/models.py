from django.contrib.auth.models import AbstractUser
from django.db import models


#При создании пользователя администратором роль нового пользователя определяется из списка
ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    ),
    role = models.CharField(
        'Роль на сайте',
        max_length=10,
        choices=ROLES,
        default='user'
    )
