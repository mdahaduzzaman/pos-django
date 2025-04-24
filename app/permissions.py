from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Custom permission to only allow users who are part of the 'manager' group.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the 'manager' group
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name="manager").exists()
        return False
