from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from coreapp.models import User, Page, Post, Tag

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "email", "first_name", "last_name", "password"]
    extra_kwargs = {'password': {'write_only': True,}}

    def validate(self, data):
         user = User(**data)
         password = data.get('password')
         errors = dict() 
         try:
             validators.validate_password(password=password, user=user)
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
         if errors:
             raise serializers.ValidationError(errors)
         return super(UserModelSerializer, self).validate(data)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password = make_password(validated_data['password'],)
        )
        user.save()
        return user


class PageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ['id', 'uuid']
        read_only_fields = ['owner',  "unblock_date", "followers", "follow_requests"]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content", "page", 'reply_to']

