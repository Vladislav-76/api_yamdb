from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet, UserViewSet, GenreViewSet,
                    CategoryViewSet, TitlesViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'titles', TitlesViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('users/<str:username>/', UserViewSet, name='user-detail'),
    path('v1/', include(router_v1.urls)),
]
