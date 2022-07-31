from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text='Описание группы', blank=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField('Год выпуска')
    genre =models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name='Катигория',
        blank=True, null=True
    )

    def __str__(self):
        return self.name