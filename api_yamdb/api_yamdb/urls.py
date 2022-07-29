from api.views import UserViewSet
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

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
    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.jwt')),
]
