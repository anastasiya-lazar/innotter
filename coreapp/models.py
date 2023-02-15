from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """
    A class implementing a User model. Username, Email, First name, Last name and password are required. Other fields are optional.
    """
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    first_name = models.CharField(('first name'), max_length=150,blank=False)
    last_name = models.CharField(('last name'),max_length=150,blank=False)
    email = models.EmailField(unique=True, blank=False)
    image_s3_path = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Tag(models.Model):
    """
    A class implementing a Tag model. Has a single field name that is required.
    """
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    """
    A class implementing a Page model. Has relationships with User and Tag models. Name field is required. Uuid and is_private fields have a default value. Other fields are optional.
    """
    name = models.CharField(max_length=80,  blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', related_name='pages', blank=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('User', related_name='follows', blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('User', related_name='requests', blank=True)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner}'s {self.name}"


class Post(models.Model):
    """
    A class implementing a Post model. Has relationships with Page and Post models. Content field is required.
    """
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180, blank=False)
    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content