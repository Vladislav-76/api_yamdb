from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class AuthSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthTokenSerializer(serializers.ModelSerializer):
    confirmation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'confirmation')
