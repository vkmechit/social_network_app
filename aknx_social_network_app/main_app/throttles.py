from rest_framework.throttling import UserRateThrottle


class FriendRequestRateThrottle(UserRateThrottle):
    """
    Throttle class that limits the rate of friend requests.
    This class inherits from UserRateThrottle and sets a specific 
    rate limit for sending friend requests to three requests per minute. 
    It is used to prevent abuse of the friend request feature in the application.
    
    Attributes:
        rate (str): The maximum number of requests allowed per user within a specified time frame.
    """

    rate = '3/min'
#     cache_format = 'friend_request_throttle_%s' 
    
#     def get_cache_key(self, request, view):
#         """
#         Returns the cache key for the request.

#         This method generates a unique cache key based on the user's ID, allowing for user-specific throttling.
#         """
#         if request.user.is_authenticated:
#             cache_key = self.cache_format % request.user.id
#             logger.debug(f"Cache key for user {request.user.id}: {cache_key}")
#             return self.cache_format % request.user.id
#         return None  # No throttling for unauthenticated users


# class FriendRequestRateThrottle(UserRateThrottle):
#     scope = 'friend_request'