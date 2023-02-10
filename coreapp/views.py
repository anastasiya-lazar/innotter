from django.shortcuts import render
from rest_framework import viewsets, permissions
from coreapp.models import User, Page, Tag, Post 
from coreapp.serializers import UserModelSerializer, PageModelSerializer, TagModelSerializer, PostModelSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageModelSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer