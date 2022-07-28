from rest_framework import viewsets, permissions
from reviews.models import User
from .serializers import AuthSignupSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters



from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAdminUser, )


@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = AuthSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            #token = default_token_generator.make_token(serializer)
            #uid = urlsafe_base64_encode(force_bytes(serializer.pk))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
