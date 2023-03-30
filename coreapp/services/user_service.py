from coreapp.models import User, Page
import datetime
from coreapp.services.aws_s3_service import S3Service
import django.contrib.auth.password_validation as validators
from rest_framework import exceptions
from rest_framework import serializers
import copy
from django.contrib.auth.hashers import make_password


class UserService:
    def password_validation(self, value, instance):
        try:
            validators.validate_password(value, instance)
        except exceptions.ValidationError:
            raise serializers.ValidationError
        validators.validate_password(value, instance)
        return value

    def change_user_status(self, user, role):
        if role == User.Roles.MODERATOR:
            user.is_staff = True
            user.is_superuser = False
        elif role == User.Roles.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif role == User.Roles.USER:
            user.is_staff = False
            user.is_superuser = False
        user.save(update_fields=["is_staff", "is_superuser"])

    def block_users_pages(self, user, serializer):
        if serializer.data["is_blocked"]:
            Page.objects.filter(owner=user).update(unblock_date=datetime.datetime.max)
        else:
            Page.objects.filter(owner=user).update(unblock_date=None)

    def upload_user_image_to_s3(self, image, user):
        object_name = f"user_{user.id}_image"
        try:
            S3Service().upload_file(file_name=image, object_name=object_name)
            user.image_s3_path = object_name
            user.save()
        except KeyError:
            image = None

    def get_image(self, validated_data):
        try:
            image = copy.copy(validated_data["image"])
            validated_data.pop("image", None)
        except KeyError:
            image = None
        return image

    def create_user(self, validated_data, serializer):
        validated_data["password"] = make_password(validated_data["password"], )
        image = self.get_image(validated_data)
        user = serializer.save()
        if image:
            UserService().upload_user_image_to_s3(image, user)
