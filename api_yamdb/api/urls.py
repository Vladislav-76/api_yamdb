from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, UsernameViewSet, MeViewSet, ReviewViewSet,
                    CommentViewSet,
                    GenreViewSet, CategoryViewSet, TitlesViewSet)

router_v1 = DefaultRouter()

router_v1.register(
    'users/<str:username>/', UsernameViewSet, basename='username')
router_v1.register('users/<me>/', MeViewSet, basename='me')
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

    path('v1/auth/signup/', MeViewSet.user_create, name='user_create'),
    path('v1/auth/token/', MeViewSet.token_create, name='token_create'),
    path('v1/', include(router_v1.urls)),
]
