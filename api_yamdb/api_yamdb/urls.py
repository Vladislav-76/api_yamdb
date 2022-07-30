from api.views import MeViewSet, UserViewSet, UsernameViewSet
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users/<str:username>/', UsernameViewSet, basename='username')
router.register('users/<me>/', MeViewSet, basename='me')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls)),
    path('auth/', include('api.urls', namespace='auth')),
]
