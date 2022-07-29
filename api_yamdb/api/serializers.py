from rest_framework import serializers
from reviews.models import User
#from .views import confirmation_code


confirmation_code = "1234567890"


class UserSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role', 'code')

    def get_code(self, obj):
        return confirmation_code


class AuthSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', "confirmation_code")
