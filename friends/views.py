from datetime import timedelta
from django.forms import ValidationError
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, permissions, views

from friends.models import Friend, FriendRequest
from friends.serializers import FriendRequestAcceptSerializer, FriendRequestSerializer
from social_net.settings import FRIEND_REQUEST_PER_MINUTES
from users.models import CustomUser
from users.serializers import UserSerializer

# Create your views here.


class FriendRequestView(generics.CreateAPIView):
    """Send friend request"""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user_id = self.request.data.get("to_user")
        to_user = CustomUser.objects.get(id=to_user_id)

        if (
            FriendRequest.objects.filter(from_user=from_user, to_user=to_user).all()
            or FriendRequest.objects.filter(from_user=to_user, to_user=from_user).all()
        ):
            raise ValidationError("Friend Request already sent.")

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if (
            FriendRequest.objects.filter(
                from_user=from_user, created_at__gte=one_minute_ago
            ).count()
            >= FRIEND_REQUEST_PER_MINUTES
        ):
            raise ValidationError(
                "You have reached the limit of 3 friend requests per minute."
            )
        serializer.save(from_user=from_user, to_user=to_user)


class AcceptFriendRequestView(generics.UpdateAPIView):
    """Accept friend request"""
    serializer_class = FriendRequestAcceptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from_user_id = self.request.data.get("from_user")
        from_user_obj = CustomUser.objects.get(id=from_user_id)
        return FriendRequest.objects.filter(
            to_user=self.request.user, from_user=from_user_obj, status="pending"
        )

    def perform_update(self, serializer):
        instance = serializer.save(status="accepted")
        Friend.objects.create(user=instance.from_user, friend=instance.to_user)


class RejectFriendRequestView(generics.UpdateAPIView):
    """Reject Friend request"""
    serializer_class = FriendRequestAcceptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from_user_id = self.request.data.get("from_user")
        from_user_obj = CustomUser.objects.get(id=from_user_id)
        return FriendRequest.objects.filter(
            to_user=self.request.user, from_user=from_user_obj, status="pending"
        )

    def perform_update(self, serializer):
        serializer.save(status="rejected")

class ListFriendsView(generics.ListAPIView):
    """List accepted friends list"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        friends = set(
            [
                friend.friend
                for friend in Friend.objects.filter(user=self.request.user).all()
            ]
            + [
                friend.user
                for friend in Friend.objects.filter(friend=self.request.user).all()
            ]
        )
        friends.discard(self.request.user)
        return friends

class ListPendingRequestView(generics.ListAPIView):
    """Pending friends list"""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status="pending").all()