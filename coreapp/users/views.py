from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import logout
from coreapp.models import User
from coreapp.users.serializers import (
    UserLikedPostsSerializer, UserChangeRoleModelSerializer, RefreshSerializer,
    TokenSerializer, UserBlockModelSerializer, LoginSerializer,
    UserListModelSerializer, UserRetrieveModelSerializer, UserModelSerializer
)
from coreapp.services.auth_service import AuthService
from coreapp.services.permissions import UserModelPermission
from coreapp.services.user_service import UserService


class AuthenticationViewSet(viewsets.GenericViewSet):
    """
    A viewset for instances of User model that provides `login()`, `refresh()`, `logout()` actions.
    """

    serializer_classes = {
        "login": LoginSerializer,
        "refresh": RefreshSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens_data = AuthService().get_user_and_generate_tokens(email=serializer.validated_data["email"])
        return Response(TokenSerializer(tokens_data).data)

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = AuthService().validate_token(serializer.validated_data["refresh_token"])
        tokens_data = AuthService().generate_access_and_refresh_token(user_id)
        return Response(TokenSerializer(tokens_data).data)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response("User Logged out successfully")


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset for instances of User model that provides `create()`, `retrieve()`,
    `partial_update()`, `destroy()`, `list()`, `list_of_liked_posts()`, `block_user()`,  `change_user_role()` actions.
    """
    queryset = User.objects.all()

    def get_queryset(self):
        if self.action == "list":
            return User.objects.exclude(is_blocked=True)
        return self.queryset

    http_method_names = ("get", "post", "patch", "delete")
    serializer_classes = {
        "list": UserListModelSerializer,
        "retrieve": UserRetrieveModelSerializer,
        "block_user": UserBlockModelSerializer,
        "change_user_role": UserChangeRoleModelSerializer,
        "list_of_liked_posts": UserLikedPostsSerializer,
        "default": UserModelSerializer,
    }
    permission_classes = [UserModelPermission]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes["default"])

    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser])
    def block_user(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        UserService().block_users_pages(user, serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser])
    def change_user_role(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def list_of_liked_posts(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
