from rest_framework import viewsets, permissions, mixins
from coreapp.models import User, Page, Tag, Post 
from coreapp import serializers
from coreapp.authentication import create_refresh_token, create_access_token, validate_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException


class LoginView(APIView):
    def post(self, request):
        user=User.objects.get(email=request.data['email'])
        if not user:
            raise APIException ('Invalid Credentials')
        if not user.check_password(request.data['password']):
            raise APIException ('Invalid Credentials')
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()
        response.set_cookie(key='refresh-token', value = refresh_token, httponly=True)
        response.data = {
                'access-token': access_token,
            }
        return response


class RefreshAPIView(APIView):   
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh-token')
        id = validate_token(refresh_token)
        access_token = create_access_token(id)
        refresh_token = create_refresh_token(id)
        response = Response()
        response.set_cookie(key='refresh-token', value = refresh_token, httponly=True)
        response.data = {
                'access-token': access_token,
            }
        return response


class LogoutAPIView(APIView):
    def post(self, _):
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



