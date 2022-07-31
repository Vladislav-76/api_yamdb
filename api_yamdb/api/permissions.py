from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('POST', 'PATCH', 'DELETE'):
            if request.user.role == 'admin':
                return True
        return False
