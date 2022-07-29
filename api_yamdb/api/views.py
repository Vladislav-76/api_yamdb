from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Title, Review
from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from .permissions import IsAuthorModerAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def title_from_url(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        new_queryset = self.title_from_url().reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_from_url()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def review_from_url(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        new_queryset = self.review_from_url().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_from_url()
        )
