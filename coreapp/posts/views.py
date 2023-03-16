from rest_framework import viewsets, mixins
from coreapp.models import Post
from coreapp.posts.serializers import (
    PostCreateModelSerializer, PostLikeModelSerializer,
    PostUpdateModelSerializer, PostRetrieveModelSerializer,
    PostModelSerializer
)
from coreapp.services.permissions import PostModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset for instances of Post model that provides `create()`, `retrieve()`, `partial_update()`, `destroy()`, list()` and `like_and_unlike_post()` actions.
    """
    queryset = Post.objects.all()

    def get_queryset(self):
        if self.action == "list":
            return Post.objects.filter(page__unblock_date=None)
        return self.queryset

    http_method_names = ("get", "post", "patch", "delete")

    permission_classes = [PostModelPermission]

    serializer_classes = {
        "partial_update": PostUpdateModelSerializer,
        "retrieve": PostRetrieveModelSerializer,
        "create": PostCreateModelSerializer,
        "like_and_unlike_post": PostLikeModelSerializer,
        "default": PostModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes["default"])

    @action(detail=True, methods=["patch"])
    def like_and_unlike_post(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
