from rest_framework import serializers
from reviews.models import Review, Comment


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
