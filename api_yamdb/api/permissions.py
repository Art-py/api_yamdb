from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsReadOnlyOrIsAuthorOrIsAdminOrIsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        # Проверяем, что пользователь отправил безопасный запрос,
        # или он аутентифицирован.
        # Так как без данного метода не аутентифицированному пользователю
        # будет разрешено отправлять POST запросы,
        # Что противоречит логике пермишена.
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated and (
                    request.user == obj.author
                    or request.user.is_admin
                    or request.user.is_moderator
                )
            )
        )
