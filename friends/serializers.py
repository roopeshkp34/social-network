from rest_framework import serializers

from friends.models import FriendRequest
from users.models import CustomUser
from users.serializers import UserSerializer

class FriendRequestSerializer(serializers.ModelSerializer):
    """Friend request serializer"""
    from_user = UserSerializer(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

class FriendRequestAcceptSerializer(serializers.ModelSerializer):
    """Friend request accept serializer."""
    from_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']