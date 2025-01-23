from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
import logging

logger = logging.getLogger(__name__)


#======================================== User Check Out ============================================

class CheckOwnershipPermission(BasePermission):
    message = "You are not allowed to make changes because you are not the owner."
    
    def has_permission(self, request: Request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user or obj.user == request.user


#======================================== User Check Out Premium ====================================

class IsPremiumOrOwnerPermission(BasePermission):
    message = "You are not allowed, you need to be the owner or have a premium account."

    def has_permission(self, request: Request, view):
        if request.user.is_authenticated:
            # Refresh the user object to ensure the latest data
            request.user.refresh_from_db()
            logger.debug(f"has_permission: User: {request.user}, Authenticated: True")
            return True
        logger.debug(f"has_permission: User: Anonymous")
        return False

    def has_object_permission(self, request: Request, view, obj):
        logger.debug(f"has_object_permission invoked for User: {request.user}")
        # This condition allows HEAD and OPTIONS requests to pass through without additional permission checks, 
        # while GET requests continue to follow the default behavior and still require the has_object_permission checks.
        if request.method in SAFE_METHODS and request.method != "GET":
            logger.debug(f"Request method {request.method} is safe, allowing access.")
            return True

        if request.user.is_authenticated:
            request.user.refresh_from_db()
            is_premium = request.user.is_premium
            is_owner = obj.user == request.user
            logger.debug(f"has_object_permission: User: {request.user}, Premium: {is_premium}, Owner: {is_owner}")

            if not is_premium and not is_owner:
                error = "Permission denied due to lack of premium status and not being the owner."
                self.message = f"{error} {self.message}"
                logger.debug(error)
                return False

            logger.debug("Permission granted.")
            return True
        else:
            logger.debug("Permission denied for AnonymousUser.")
            return False
        
    
#===================================================================================================