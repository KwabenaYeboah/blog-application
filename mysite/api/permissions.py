from rest_framework import permissions

class IsCurrentUserOrAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Grant admin access to all profiles
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        
        # Grant owner of profile access
        return obj.pk == request.user.pk
        
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Grant author of a post full access
        return obj.author == request.user

