from rest_framework import serializers
from coreapp.models import Post, Page
from coreapp.pages.serializers import PageForPostModelSerializer
from coreapp.services.post_service import PostService
from coreapp.services.exceptions import InvalidPageException


class PostModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Post model
    """
    page = PageForPostModelSerializer()

    class Meta:
        model = Post
        fields = ("id", "content", "page", "reply_to", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class PostCreateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model(create action)
    """

    class Meta:
        model = Post
        fields = ("id", "content", "page", "reply_to")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        page_id = validated_data["page"].id
        if Page.objects.filter(id=page_id, unblock_date__isnull=True).exists():
            return validated_data
        else:
            raise InvalidPageException

    def create(self, validated_data):
        post = super().create(validated_data)
        PostService().send_new_post_notification_email(post)
        return post


class PostRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (retrieve action)
    """
    page = PageForPostModelSerializer()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "content", "page", "reply_to", "created_at", "updated_at", "likes")

    def get_likes(self, obj):
        return obj.likes.count()


class PostUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (update action)
    """

    class Meta:
        model = Post
        fields = ("content",)


class PostLikeModelSerializer(serializers.ModelSerializer):
    """
        A Serializer for Post model (like_and_unlike_post action)
    """

    to_like = serializers.BooleanField(default=False)

    class Meta:
        model = Post
        fields = ("id", "to_like", "likes")
        read_only_fields = ("likes",)

    def update(self, instance, validated_data):
        post = super().update(instance, validated_data)
        request = self.context.get("request")
        like_post = PostService().add_likes(post, validated_data, request)
        return like_post
