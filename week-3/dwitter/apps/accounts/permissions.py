from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    """
    Allow access to admin users or the user themselves.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif request.user and obj == request.user:
            return True
        return False