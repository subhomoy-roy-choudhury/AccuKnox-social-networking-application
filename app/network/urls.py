from django.urls import path
from .views import (
    SendFriendRequestView,
    FriendRequestActionView,
    ListFriendsView,
    ListPendingRequestsView,
)

urlpatterns = [
    path("friends/", ListFriendsView.as_view(), name="list-friends"),
    path("friends/requests/", ListPendingRequestsView.as_view(), name="list-requests"),
    path(
        "friends/requests/send/", SendFriendRequestView.as_view(), name="send-request"
    ),
    path(
        "friends/requests/<int:pk>/<str:action>/",
        FriendRequestActionView.as_view(),
        name="update-request",
    ),
]
