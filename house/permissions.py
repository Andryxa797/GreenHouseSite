from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
        )


class IsOwnerOrReadOnlyForAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated or request.user.is_staff:
            return True

