from rest_framework import routers
from django.urls import include, path
from .views import GenreViewSet, CategoryViewSet, TitlesViewSet


router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitlesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]