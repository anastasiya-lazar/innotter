from rest_framework import serializers
from coreapp.models import User
from coreapp.services.exceptions import InvalidCredentialsException, UserNotFoundException
from coreapp.services.auth_service import AuthService
from coreapp.services.user_service import UserService
from coreapp.services.aws_s3_service import S3Service


class UserPresignedURLMixin(serializers.ModelSerializer):
    """
        A Mixin for instances of User model for inheriting to get presigned url of object's image
    """
    image_presigned_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("image_presigned_url",)

    def get_image_presigned_url(self, obj):
        object_name = str(obj.image_s3_path)
        return S3Service().create_presigned_url(object_name=object_name)


class LoginSerializer(serializers.Serializer):
    """
        A serializer for instances of User model that provides `login()` actions.
    """
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.filter(email=email).first()
        if not user:
            raise UserNotFoundException
        if not user.check_password(password):
            raise InvalidCredentialsException
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
        refresh_token = validated_data["refresh_token"]
        AuthService().validate_token(refresh_token)
        return validated_data


class UserBlockModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model For Role ADMIN to block a user
    """

    class Meta:
        model = User
        fields = ("id", "is_blocked")


class UserChangeRoleModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model For Role ADMIN to change user role
    """

    class Meta:
        model = User
        fields = ("id", "role")

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        role = validated_data["role"]
        UserService().change_user_status(user, role)
        return user


class UserListModelSerializer(UserPresignedURLMixin):
    """
    A Serializer for User model (list action)
    """
    class Meta(UserPresignedURLMixin.Meta):
        fields = ("id", "first_name", "last_name", "username") + UserPresignedURLMixin.Meta.fields


class UserModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for User model with implementations of "validate()" - for password validation and "create()" methods
    """
    image = serializers.FileField(max_length=256, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "title", "password", "image")
        extra_kwargs = {
            "password": {"write_only": True, },
            "email": {"write_only": True, }
        }

    def validate_password(self, value):
        value = UserService().password_validation(value=value, instance=self.instance)
        return value


class UserUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for User model with implementations of "validate()" - for password validation and "create()" methods
    """
    image = serializers.FileField(max_length=256, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "title", "password", "image")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"write_only": True, "required": False},
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate_password(self, value):
        value = UserService().password_validation(value=value, instance=self.instance)
        return value

    def update(self, instance, validated_data):
        image = UserService().get_image(validated_data)
        user = super().update(instance, validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        if image:
            UserService().upload_user_image_to_s3(image, user)
        return user


class UserRetrieveModelSerializer(UserPresignedURLMixin):
    """
    A Serializer for User model (retrieve action)
    """

    class Meta(UserPresignedURLMixin.Meta):
        fields = ("id", "username", "first_name", "last_name", "title", "image_s3_path", "date_joined",
                  "is_blocked",) + UserPresignedURLMixin.Meta.fields


class UserLikedPostsSerializer(serializers.ModelSerializer):
    """
        A Serializer for User model (list_of_liked_posts action)
    """

    class Meta:
        model = User
        fields = ("id", "liked")
        depth = 1
