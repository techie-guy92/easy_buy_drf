from rest_framework.permissions import BasePermission, SAFE_METHODS  
from rest_framework.request import Request


class UserCheckOut(BasePermission):
    message = "You are not allowed"
    
    # Checks if the user is authenticated for all types of requests.
    def has_permission(self, request: Request, view):
        return request.user and request.user.is_authenticated
    
    # Allows safe methods (e.g., GET) without additional checks.
    # Grants permission if the object is the user itself or if the user is related to the object (e.g., obj.user).
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # this covers cases where the obj might be either the user object itself or an object related to the user.
        return obj == request.user or obj.user == request.user



