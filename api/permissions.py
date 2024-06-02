from rest_framework import permissions


class IsCreatorOrRecipientReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.chat.users.all()
        
        return False