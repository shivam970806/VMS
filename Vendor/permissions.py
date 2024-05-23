# permissions.py
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        
        if request.method in ['PUT', 'DELETE']:
            return obj.created_by  == request.user
        
        if request.method == 'POST':
            return obj.created_by  != request.user
        
        return False
