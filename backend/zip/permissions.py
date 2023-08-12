from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWriterOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            # Allow update (PATCH, PUT, DELETE) only for the writer of the object or an admin
            return obj.user == request.user or request.user.is_staff
        else:
            # Allow other methods (GET, POST, DELETE) for all users
            return True


class IsReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Allow POST for all authenticated users
        if request.method == "POST" and request.user.is_authenticated:
            return True

        # Allow other non-safe methods only for admin users
        return request.user and request.user.is_staff
