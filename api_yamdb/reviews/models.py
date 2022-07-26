from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Titles(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.DateTimeField(
        'Год выпуска', auto_now_add=True, db_index=True
    )
    description = models.TextField(help_text='Описание', blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField(help_text='Текст review')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    titles = models.ForeignKey(
        Titles, on_delete=models.SET_NULL,
        related_name="review", blank=True, null=True
    )
    score = models.IntegerField(help_text='Оценка score')


    def __str__(self):
        return self.text[:15]

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
