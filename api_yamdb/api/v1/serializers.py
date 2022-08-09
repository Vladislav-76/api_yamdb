from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from reviews.models import (Review, Comment, Genre, Category, Title)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /users/"""
    lookup_field = 'username'

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class AuthSignupSerializer(serializers.Serializer):
    """Сериализатор для эндпойнта /auth/signup/"""
    email = serializers.EmailField(
        max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150, allow_blank=False)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя ''me'' в качестве username запрещено!')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Tакой username уже существует!')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Неверно указан email!')
        return value


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор для эндпойнта /auth/token/"""
    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(max_length=99, allow_blank=False)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /genres/"""
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /categories/"""
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор чтения для эндпойнта /titles/"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор записи для эндпойнта /titles/"""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    def validate_year(self, value):
        year = datetime.today().year
        if value > year:
            raise serializers.ValidationError('Год указан неверно!')
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /reviews/"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author', 'pub_date')

    def validate(self, data):
        if self.context['request'].stream.method != 'POST':
            return data
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        queryset = Review.objects.filter(author=author, title=title_id)
        if queryset.exists() is True:
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /comments/"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'pub_date')
