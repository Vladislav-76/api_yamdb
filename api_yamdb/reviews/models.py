from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'Юзер'),
    ('moderator', 'Модератор'),
    ('admin', 'Адинистратор'),
)


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True,)
    # добавил поле с выбором значений
    role = models.CharField(max_length=10, choices=ROLES, default='user')


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):  # убрал множественное число
    name = models.CharField('Название', max_length=200)
    # изменил тип поля, убрал автоустановку
    year = models.IntegerField('Год выпуска', db_index=True)
    description = models.TextField(help_text='Описание', blank=True)
    # изменил тип поля
    genre = models.ManyToManyField(Genre, through='Title_genre')
    # добавил blank=True, null=True
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    def __str__(self):
        return self.name  # поправил ссылку на поле


class Title_genre(models.Model):  # создал модель для связи many to many
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField(help_text='Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    # поправил множественное число, установил CASCADE
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews"
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
    text = models.TextField(help_text='Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
