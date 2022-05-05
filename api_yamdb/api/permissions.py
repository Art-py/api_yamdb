from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class HasObjectPermissionToHasPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(HasObjectPermissionToHasPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(HasObjectPermissionToHasPermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.MODERATOR
        )


class IsReadOnly(HasObjectPermissionToHasPermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
