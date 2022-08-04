from rest_framework import serializers
from django.db.models import Avg
from datetime import datetime
from reviews.models import (Review, Comment, User, Genre, Category,
                            Title)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /users/"""
    lookup_field = 'username'

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /users/me/"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class AuthSignupSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпойнта /auth/signup/"""
    email = serializers.EmailField(
        max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150, allow_blank=False)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя ''me'' в качестве username запрещено.')
        return data


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор для эндпойнта /auth/token/"""
    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(max_length=30, allow_blank=False)


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
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']

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
    rating = serializers.SerializerMethodField()

    def validate_year(self, value):
        year = datetime.today().year
        if value > year:
            raise serializers.ValidationError('Неверная дата')
        return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
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
        if self.context['request'].stream.method == 'POST':
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
