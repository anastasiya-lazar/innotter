from rest_framework import serializers
from coreapp.models import Tag


class TagModelSerializer(serializers.ModelSerializer):
    """
    A Serializer for Tag model
    """

    class Meta:
        model = Tag
        fields = ("name",)
