from rest_framework.permissions import BasePermission
from accounts.models import User

class IsManager(BasePermission):
    """Разрешаем доступ только пользователям с role == manager"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.MANAGER)
