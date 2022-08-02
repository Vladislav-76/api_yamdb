from rest_framework import serializers
from django.db.models import Avg
from reviews.models import (Review, Comment, User, Genre, Category,
                            Title, Title_genre)

from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    lookup_field = 'username'

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class AuthSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254, allow_blank=False,
    )
    username = serializers.CharField(
        max_length=150, allow_blank=False,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя ''me'' в качестве username запрещено.')
        return data


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(max_length=30, allow_blank=False)


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    category = CategorySerializer()  # SerializerMethodField()

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']

    def get_genre(self, obj):
        queryset = Title_genre.objects.filter(title=obj.id)
        genres = []
        for position in queryset:
            name = position.genre.name
            slug = position.genre.slug
            genres.append({"name": name, "slug": slug})
        return genres

    # def get_category(self, obj):
    #     category = get_object_or_404(Category, titles=obj.id)
    #     return {"name": category.name, "slug": category.slug}

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.SerializerMethodField()


    def create(self, validated_data):
        if 'genre' not in validated_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            Title_genre.objects.create(
                genre=current_genre, title=title)
        return title

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        year = datetime.today().year

        if value > year:
            raise serializers.ValidationError(
                'Проверьте год произведения'
            )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'pub_date')
