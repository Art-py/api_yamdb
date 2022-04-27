from rest_framework import permissions
from reviews.models import User


class IsAuthor(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        return obj.author == request.user


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user.role == User.ADMIN


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user.role == User.MODERATOR


class IsReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.method in permissions.SAFE_METHODS
