from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Только администратор"""
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'admin')


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PATCH', 'DELETE'):
            if request.user.role in ['moderator', 'admin']:
                return True
        return obj.author == request.user
