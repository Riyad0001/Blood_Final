from rest_framework import permissions

class IsEventCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET requests to all, but restrict writes to the creator
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user