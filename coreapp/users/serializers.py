from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from coreapp.models import User
from coreapp.services.exceptions import InvalidCredentialsException, UserNotFoundException
from coreapp.services.auth_service import AuthService
from coreapp.services.user_service import change_user_status


class LoginSerializer(serializers.Serializer):
    """
        A serializer for instances of User model that provides `login()` actions.
    """
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise InvalidCredentialsException
        except User.DoesNotExist:
            raise UserNotFoundException
        return validated_data


class TokenSerializer(serializers.Serializer):
    """
        A serializer for returning tokens
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    """
        A serializer for instances of User model that provides `refresh()` actions.
    """
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        refresh_token = validated_data['refresh_token']
        AuthService().validate_token(refresh_token)
        return validated_data


class UserBlockModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model For Role ADMIN to block a user
    """

    class Meta:
        model = User
        fields = ["id", "is_blocked"]


class UserChangeRoleModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model For Role ADMIN to change user role
    """

    class Meta:
        model = User
        fields = ["id", "role"]

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        role = validated_data["role"]
        change_user_status(user, role)
        return user


class UserListModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model (list action)
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class UserModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for User model with implementations of 'validate()' - for password validation and 'create()' methods
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "title", "password"]
        extra_kwargs = {"password": {"write_only": True, },
                        "email": {"write_only": True, }
                        }

    def validate(self, data):
        user = User(**data)
        password = data.get("password")
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)
        except errors:
            raise serializers.ValidationError(errors)
        return super(UserModelSerializer, self).validate(data)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"], )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        return user


class UserRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model (retrieve action)
    """

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "title", "date_joined", "is_blocked"]


class UserLikedPostsSerializer(serializers.ModelSerializer):
    """
        A Serializer for User model (list_of_liked_posts action)
    """

    class Meta:
        model = User
        fields = ["id", "liked"]
        depth = 1
