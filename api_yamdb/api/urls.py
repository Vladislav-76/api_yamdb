from rest_framework import routers
from django.urls import include, path
from rest_framework.authtoken import views
from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitlesViewSet)
router.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews'
)
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]