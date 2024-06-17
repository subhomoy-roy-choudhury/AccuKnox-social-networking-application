from rest_framework import serializers
from .models import Friendship

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']