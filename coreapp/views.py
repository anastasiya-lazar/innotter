from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from coreapp.models import User, Page, Tag, Post 
from coreapp import serializers


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for instances of User model that provides `create()`, `retrieve()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_classes = { 
        'list': serializers.UserListModelSerializer,
        'retrieve': serializers.UserRetrieveModelSerializer,
        'default':  serializers.UserModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes ['default'])


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for instances of Page model that provides `create()`, `retrieve()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = Page.objects.all()
    serializer_class = serializers.PageModelSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_classes = { 
        'partial_update': serializers.PageUpdateModelSerializer,
        'list': serializers.PageListModelSerializer,
        'retrieve': serializers.PageRetrieveModelSerializer,
        'default':  serializers.PageModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes ['default'])


class TagViewSet(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    A viewset for instances of Tag model that provides `create()`, `destroy()` and `list()` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagModelSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for instances of Post model that provides `create()`, `retrieve()`, `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = Post.objects.all()
   
    http_method_names = ('get', 'post', 'patch', 'delete')

    serializer_classes = { 
        'partial_update': serializers.PostUpdateModelSerializer,
        'retrieve': serializers.PostRetrieveModelSerializer,
        'default':  serializers.PostModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes ['default'])



