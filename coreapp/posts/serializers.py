from rest_framework import serializers
from coreapp.models import Post, Page
from django.db.models import Count
from coreapp.pages.serializers import PageForPostModelSerializer
from coreapp.services.post_service import like_or_unlike
from coreapp.services.exceptions import InvalidPageException


class PostModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Post model
    """
    page = PageForPostModelSerializer()

    class Meta:
        model = Post
        fields = ["id", "content", "page", "reply_to", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostCreateModelSerializer(serializers.ModelSerializer):
    """
    A Default Serializer for Post model
    """

    class Meta:
        model = Post
        fields = ["id", "content", "page", "reply_to"]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        page_id = validated_data['page'].id
        page = Page.objects.get(id=page_id)
        if page.unblock_date:
            raise InvalidPageException
        return validated_data


class PostRetrieveModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (retrieve action)
    """
    page = PageForPostModelSerializer()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "content", "page", "reply_to", "created_at", "updated_at", "likes"]

    def get_likes(self, obj):
        q = Post.objects.all().annotate(num_likes=Count('likes'))
        return q.get(id=obj.id).num_likes


class PostUpdateModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Post model (update action)
    """

    class Meta:
        model = Post
        fields = ["content"]


class PostLikeModelSerializer(serializers.ModelSerializer):
    """
        A Serializer for Post model (like_and_unlike_post action)
    """

    to_like = serializers.BooleanField(default=False)

    class Meta:
        model = Post
        fields = ["id", "to_like", "likes"]
        read_only_fields = ["likes"]

    def update(self, instance, validated_data):
        post = super().update(instance, validated_data)
        request = self.context.get("request")
        user = request.user
        p = like_or_unlike(post, validated_data, user)
        validated_data.pop("to_like", None)
        return p
