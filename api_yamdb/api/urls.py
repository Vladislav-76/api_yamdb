from rest_framework import routers
from django.urls import include, path
from rest_framework.authtoken import views
from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitlesViewSet)