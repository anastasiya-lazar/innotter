from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from coreapp.models import Page
from coreapp.pages.serializers import (
    PageFollowSerializer, PageUpdateModelSerializer, PageListModelSerializer,
    PageListFollowRequestsSerializer, PageAcceptFollowRequestsSerializer,
    PageRetrieveModelSerializer, PageBlockModelSerializer, PageModelSerializer
)
from coreapp.services.permissions import PageModelPermission
from rest_framework import status


class PageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset for instances of Page model that provides `create()`, `retrieve()`,
    `partial_update()`, `destroy()` and `list()`, `accept_or_decline_follow_requests()`, `block_page()`,
    `follow_and_unfollow_page()`, `get_list_follow_requests()` actions.
    """
    queryset = Page.objects.all()

    def get_queryset(self):
        if self.action == "list":
            return Page.objects.filter(unblock_date=None)
        return self.queryset

    permission_classes = [PageModelPermission]

    http_method_names = ("get", "post", "patch", "delete")
    serializer_classes = {
        "partial_update": PageUpdateModelSerializer,
        "list": PageListModelSerializer,
        "retrieve": PageRetrieveModelSerializer,
        "block_page": PageBlockModelSerializer,
        "follow_and_unfollow_page": PageFollowSerializer,
        "get_list_follow_requests": PageListFollowRequestsSerializer,
        "accept_or_decline_follow_requests": PageAcceptFollowRequestsSerializer,
        "default": PageModelSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes["default"])

    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser], url_name="block_page")
    def block_page(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_name="follow_and_unfollow_page")
    def follow_and_unfollow_page(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_name="get_list_follow_requests")
    def get_list_follow_requests(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_name="accept_or_decline_follow_requests")
    def accept_or_decline_follow_requests(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
