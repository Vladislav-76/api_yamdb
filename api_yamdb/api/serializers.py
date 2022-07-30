from rest_framework import serializers
from django.db.models import Avg
from reviews.models import Review, Comment, User, Genre, Category, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']

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
