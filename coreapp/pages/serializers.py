from rest_framework import serializers
from coreapp.models import Page
from coreapp.tags.serializers import TagModelSerializer
from coreapp.users.serializers import UserModelSerializer, UserListModelSerializer
from coreapp.services.page_service import page_follow_unfollow, accept_decline_follow_requests


class PageForPostModelSerializer(serializers.ModelSerializer):
    """
        A Serializer for Page model for using in nested serializer
    """

    class Meta:
        model = Page
        fields = ("name", "description", "image")


class PageBlockModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model For Role ADMIN and MODERATOR to block a page for a certain period of time
    """

    class Meta:
        model = Page
        fields = ("id", "unblock_date")


class PageModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Page model with implementation of 'create()' method
    """

    class Meta:
        model = Page
        fields = ("id", "name", "description", "image", "is_private", "owner", "tags")
        read_only_fields = ("id", "owner")

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
        fields = ("id", "name", "description", "image", "owner", "is_private", "tags")


class PageRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (retrieve action)
    """
    tags = TagModelSerializer(many=True)
    owner = UserModelSerializer()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("name", "description", "image", "owner", "is_private", "tags", "followers")

    def get_followers(self, obj):
        return obj.followers.count()


class PageUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (update action)
    """

    class Meta:
        model = Page
        fields = ("name", "description", "image", "is_private", "tags")


class PageOwnerModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (owner)
    """
    owner = UserListModelSerializer()

    class Meta:
        model = Page
        fields = ("name", "owner")


class PageFollowSerializer(serializers.ModelSerializer):
    """
    A Serializer for Page model (follow_and_unfollow_page action)
    """
    follow = serializers.BooleanField(default=False)

    class Meta:
        model = Page
        fields = ("id", "follow", "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")

    def update(self, instance, validated_data):
        page = super().update(instance, validated_data)
        request = self.context.get("request")
        user = request.user
        page = page_follow_unfollow(page, user, validated_data)
        validated_data.pop('follow', None)
        return page


class PageListFollowRequestsSerializer(serializers.ModelSerializer):
    """
        A Serializer for Page model (get_list_follow_requests action)
    """
    follow_requests = UserListModelSerializer(many=True)

    class Meta:
        model = Page
        fields = ("id", "follow_requests")


class PageAcceptFollowRequestsSerializer(serializers.ModelSerializer):
    """
        A Serializer for Page model (accept_or_decline_follow_requests action)
    """
    accept = serializers.BooleanField(default=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Page
        fields = ("id", "accept", "user_id", "follow_requests", "followers")
        read_only_fields = ("follow_requests", "followers")

    def update(self, instance, validated_data):
        page = super().update(instance, validated_data)
        page_instance = accept_decline_follow_requests(validated_data, page)
        return page_instance
