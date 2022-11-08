from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Allow access to admin users or the objects owner (assuming that the object has a user attribute
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif request.user and (obj == request.user or obj.user == request.user):
            return True
        return False
