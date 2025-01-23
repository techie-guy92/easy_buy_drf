from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
import logging

logger = logging.getLogger(__name__)


#======================================== User Check Out ============================================

class UserCheckOut(BasePermission):
    message = "You are not allowed."
    
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


#======================================== User Check Out Premium ====================================

class UserCheckOutPremium(BasePermission):
    message = "You are not allowed, you need to have a premium account or be the owner."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Refresh the user object to ensure the latest data
            request.user.refresh_from_db()
            logger.debug(f"has_permission: User: {request.user}, Authenticated: True")
            return True
        logger.debug(f"has_permission: User: Anonymous")
        return False

    def has_object_permission(self, request, view, obj):
        logger.debug(f"has_object_permission invoked for User: {request.user}")

        if request.method in SAFE_METHODS and request.method != 'GET':
            logger.debug(f"Request method {request.method} is safe, allowing access.")
            return True

        if request.user.is_authenticated:
            # Refresh the user object to ensure the latest data
            request.user.refresh_from_db()
            is_premium = request.user.is_premium
            is_owner = obj.user == request.user
            logger.debug(f"has_object_permission: User: {request.user}, Premium: {is_premium}, Owner: {is_owner}")

            if not is_premium and not is_owner:
                self.message = "You are not allowed, you need to have a premium account or be the owner."
                logger.debug("Permission denied due to lack of premium status and not being the owner.")
                return False

            logger.debug("Permission granted.")
            return True
        else:
            logger.debug("Permission denied for AnonymousUser.")
            return False
        
    
#===================================================================================================

# Let's break down the `UserCheckOutPremium` class, which is a custom permission class extending `BasePermission` from Django REST Framework. The purpose of this class is to enforce that only authenticated users who either have a premium account or are the owners of the object can access certain views.

# ### Class Definition and Message:

# ```python
# class UserCheckOutPremium(BasePermission):
#     message = "You are not allowed, you need to have a premium account or be the owner."
# ```
# - **Purpose**: Defines the custom permission class.
# - **message**: Custom message displayed when permission is denied.

# ### has_permission Method:

# ```python
# def has_permission(self, request, view):
#     if request.user.is_authenticated:
#         # Refresh the user object to ensure the latest data
#         request.user.refresh_from_db()
#         logger.debug(f"has_permission: User: {request.user}, Authenticated: True")
#         return True
#     logger.debug(f"has_permission: User: Anonymous")
#     return False
# ```

# - **Purpose**: Determines whether the user has general permission to access the view.
# - **If authenticated**: 
#   - Refreshes the user object to get the latest data from the database using `refresh_from_db()`.
#   - Logs a debug message with the user details and returns `True`, allowing access.
# - **If not authenticated**: 
#   - Logs a debug message indicating an anonymous user and returns `False`, denying access.

# ### has_object_permission Method:

# ```python
# def has_object_permission(self, request, view, obj):
#     logger.debug(f"has_object_permission invoked for User: {request.user}")

#     if request.method in SAFE_METHODS and request.method != 'GET':
#         logger.debug(f"Request method {request.method} is safe, allowing access.")
#         return True

#     if request.user.is_authenticated:
#         # Refresh the user object to ensure the latest data
#         request.user.refresh_from_db()
#         is_premium = request.user.is_premium
#         is_owner = obj.user == request.user
#         logger.debug(f"has_object_permission: User: {request.user}, Premium: {is_premium}, Owner: {is_owner}")

#         if not is_premium and not is_owner:
#             self.message = "You are not allowed, you need to have a premium account or be the owner."
#             logger.debug("Permission denied due to lack of premium status and not being the owner.")
#             return False

#         logger.debug("Permission granted.")
#         return True
#     else:
#         logger.debug("Permission denied for AnonymousUser.")
#         return False
# ```

# - **Purpose**: Determines whether the user has permission to access a specific object.
# - **Logs**: Logs a debug message when the method is invoked.
# - **Safe Methods**: 
#   - Checks if the request method is safe (e.g., `GET`, `HEAD`, `OPTIONS`).
#   - If the method is safe and not a `GET`, logs a message and returns `True`, allowing access.
# - **If authenticated**:
#   - Refreshes the user object to get the latest data.
#   - Checks if the user is premium (`is_premium`) and if the user is the owner (`is_owner`) of the object.
#   - Logs details of the user, premium status, and ownership.
#   - If the user is neither premium nor the owner, sets the `message` and logs a denial message, returning `False`.
#   - If the user is premium or the owner, logs a grant message and returns `True`, allowing access.
# - **If not authenticated**: 
#   - Logs a denial message for an anonymous user and returns `False`.

# ### Summary:
# - **General Permission Check**: Uses `has_permission` to ensure only authenticated users can access the view.
# - **Object-Specific Permission Check**: Uses `has_object_permission` to enforce additional conditions, allowing access only if the user is a premium member or the owner of the object.
# - **Logging**: Provides detailed logging at each step to help with debugging and understanding the permission flow.

# This class ensures that only authenticated premium users or the owners of the objects can access certain views, providing a robust way to enforce access control in your application.
