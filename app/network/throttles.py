from rest_framework.throttling import UserRateThrottle

class FriendRequestRateThrottle(UserRateThrottle):
    scope = 'send_friend_request'