from rest_framework import serializers
from .models import AuthUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ("id", "username", "email", "firstname", "lastname")

    def validate_username(self, value):
        # Additional validation for username
        if not value.isalnum() and not all(x in "_ " for x in value):
            raise serializers.ValidationError(
                "Username must contain only letters, numbers, or underscores."
            )
        return value

    def validate_firstname(self, value):
        # Validate that firstname contains only letters
        if not value.isalpha():
            raise serializers.ValidationError("Firstname must contain only letters.")
        return value

    def validate_lastname(self, value):
        # Validate that lastname contains only letters
        if not value.isalpha():
            raise serializers.ValidationError("Lastname must contain only letters.")
        return value
