from rest_framework.throttling import UserRateThrottle


class FriendRequestRateThrottle(UserRateThrottle):
    """
    Throttle class that limits the rate of friend requests.
    This class inherits from UserRateThrottle and sets a specific 
    rate limit for sending friend requests to three requests per minute. 
    It is used to prevent abuse of the friend request feature in the application.
    """

    rate = '3/min'