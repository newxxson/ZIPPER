from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWriterOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT', 'DELETE']:
            # Allow update (PATCH, PUT, DELETE) only for the writer of the object or an admin
            return obj.user == request.user or request.user.is_staff
        else:
            # Allow other methods (GET, POST, DELETE) for all users
            return True
        

class IsReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Allow read-only (GET, HEAD, OPTIONS) for all users
            return True
        else:
            # Allow other methods (POST, PUT, PATCH, DELETE) only for admin users
            return request.user and request.user.is_staff