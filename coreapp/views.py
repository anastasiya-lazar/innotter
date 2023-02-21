from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from coreapp.models import User, Page, Tag, Post
from coreapp import serializers
from coreapp.authentication import create_refresh_token, create_access_token, decode_token


class AuthenticationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            response = Response()
            response.set_cookie(key='refresh-token', value=response_data['refresh_token'], httponly=True)
            response.data = {
                'access-token': response_data['access_token']
            }
            return response
        return Response(data=serializer.errors)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.COOKIES.get('refresh-token')
        if not refresh_token:
            return JsonResponse({'error': 'Please log in.'}, status=401)
        user_id =decode_token(refresh_token)
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        response = Response()
        response.set_cookie(key='refresh-token', value=refresh_token, httponly=True)
        response.data = {
            'access-token': access_token,
        }
        return response

    
    @action(detail=False, methods=['post'],  permission_classes=[permissions.IsAuthenticated])
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
