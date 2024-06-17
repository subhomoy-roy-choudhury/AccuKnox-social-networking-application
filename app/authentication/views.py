from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework.pagination import LimitOffsetPagination
from .models import AuthUser
from .serializers import AuthUserSerializer


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": AuthUserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AuthUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AuthTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data["custom_message"] = "Refresh successful"
        return response


class UserAPIView(generics.ListAPIView):
    serializer_class = AuthUserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        current_user = self.request.user
        queryset = AuthUser.objects.all().exclude(
            id=current_user.id
        )  # Exclude the current user
        keyword = self.request.query_params.get("q", None)
        if keyword:
            email_match = queryset.filter(email__iexact=keyword)
            if email_match.exists():
                return email_match
            name_match = queryset.filter(
                firstname__icontains=keyword
            ) | queryset.filter(lastname__icontains=keyword)
            return name_match
        return queryset
