from rest_framework import views, status, response, permissions
from django.db.models import Q
from .models import Friendship
from .serializers import FriendshipSerializer
from authentication.serializers import AuthUserSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.


class SendFriendRequestView(views.APIView):
    # throttle_classes = [UserRateThrottle
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get("receiver_id")
        if request.user.id == receiver_id:
            return response.Response(
                {"message": "You cannot send a friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Friendship.objects.filter(
            sender=request.user, receiver_id=receiver_id
        ).exists():
            return response.Response(
                {"message": "Friend request already sent."},
                status=status.HTTP_409_CONFLICT,
            )

        friendship = Friendship.objects.create(
            sender=request.user, receiver_id=receiver_id
        )
        serializer = FriendshipSerializer(friendship)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestActionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def post(self, request, pk, action):
        friendship = Friendship.objects.filter(id=pk, receiver=request.user).first()
        if not friendship:
            return response.Response(
                {"message": "Friend request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if action == "accept":
            friendship.status = "accepted"
        elif action == "reject":
            friendship.status = "rejected"
        else:
            return response.Response(
                {"message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST
            )
        friendship.save()
        return response.Response(
            {"message": f"Friend request {action}ed."}, status=status.HTTP_200_OK
        )


class ListFriendsView(views.APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = Friendship.objects.filter(
            Q(sender=request.user, status="accepted")
            | Q(receiver=request.user, status="accepted")
        )
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(friends, request)
        friend_users = [
            friend.receiver if friend.sender == request.user else friend.sender
            for friend in result_page
        ]
        serializer = AuthUserSerializer(friend_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class ListPendingRequestsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = Friendship.objects.filter(
            receiver=request.user, status="sent"
        )
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(pending_requests, request)
        serializer = FriendshipSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
