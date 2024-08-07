"""User Permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only the objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same."""
        return request.user == obj


class IsSuperuser(BasePermission):
    """Allow access only for superusers."""

    def has_object_permission(self, request, view, obj):
        """Check if user is superuser"""
        return obj.is_superuser
