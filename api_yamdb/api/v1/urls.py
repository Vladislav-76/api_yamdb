from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, ReviewViewSet,
                    CommentViewSet, user_create, token_create,
                    GenreViewSet, CategoryViewSet, TitlesViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/signup/', user_create, name='user_create'),
    path('auth/token/', token_create, name='token_create'),
    path('', include(router_v1.urls)),
]
