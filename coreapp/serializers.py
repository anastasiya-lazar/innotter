from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from coreapp.models import User, Page, Post, Tag


class UserListModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model (list action)
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


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
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
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


class TagModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Tag model 
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PageModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Page model with implementation of 'create()' method
    """

    class Meta:
        model = Page
        fields = ["name", "description", "image", "is_private", "owner", "tags"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class PageListModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (list action)
    """
    tags = TagModelSerializer(many=True)
    owner = UserModelSerializer()

    class Meta:
        model = Page
        fields = ["id", "name", "description", "image", "owner", "is_private", "tags"]


class PageRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (retrieve action)
    """
    tags = TagModelSerializer(many=True)
    owner = UserModelSerializer()

    class Meta:
        model = Page
        fields = ["id", "name", "description", "image", "owner", "is_private", "tags", "followers", "follow_requests"]


class PageUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (update action)
    """

    class Meta:
        model = Page
        fields = ["name", "description", "image", "is_private", "tags", "followers", "follow_requests"]


class PageOwnerModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (owner)
    """
    owner = UserListModelSerializer()

    class Meta:
        model = Page
        fields = ["owner"]


class UserRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for User model (retrieve action)
    """
    pages = PageModelSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "title", "date_joined", "pages"]


class PostModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Post model
    """

    class Meta:
        model = Post
        fields = ["id", "content", "page", "reply_to", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (retrieve action)
    """
    page = PageOwnerModelSerializer()
    reply_to = PostModelSerializer()

    class Meta:
        model = Post
        read_only_fields = ["id", "created_at", "updated_at"]
        fields = ["id", "content", "page", "reply_to", "created_at", "updated_at"]


class PostUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (update action)
    """

    class Meta:
        model = Post
        fields = ["content"]
