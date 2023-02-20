from rest_framework import viewsets, permissions, mixins
from coreapp.models import User, Page, Tag, Post
from coreapp import serializers
from coreapp.authentication import create_refresh_token, create_access_token, decode_token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class AuthenticationViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        if not request.data.get('email') or not request.data.get('password'):
            raise APIException('Email and password can not be blank')
        try:
            user = User.objects.get(email=request.data['email'])
            if not user.check_password(request.data['password']):
                raise APIException('Invalid Credentials')
        except User.DoesNotExist:
            raise APIException('User does not exist. Invalid Credentials')
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()
        response.set_cookie(key='refresh-token', value=refresh_token, httponly=True)
        response.data = {
            'access-token': access_token,
        }
        return response

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.COOKIES.get('refresh-token')
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token is missing'}, status=401)
        id =decode_token(refresh_token)
        access_token = create_access_token(id)
        refresh_token = create_refresh_token(id)
        response = Response()
        response.set_cookie(key='refresh-token', value=refresh_token, httponly=True)
        response.data = {
            'access-token': access_token,
        }
        return response
       
    @action(detail=False, methods=['post'])
    def logout(self, _):
            response = Response()
            response.delete_cookie(key="refresh-token")
            response.data = {
                'message': 'success'
            }
            return response


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
        'default': serializers.UserModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes['default'])


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
        'default': serializers.PageModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes['default'])


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
        'default': serializers.PostModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes['default'])
