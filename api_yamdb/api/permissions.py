from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Только администратор"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'admin')
