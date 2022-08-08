from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'Юзер'),
    ('moderator', 'Модератор'),
    ('admin', 'Адинистратор'),
)


class User(AbstractUser):
    username = models.SlugField(max_length=150, unique=True, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        verbose_name='Биография', max_length=2000, blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='user')

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ['id']
