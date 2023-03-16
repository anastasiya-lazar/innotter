from rest_framework import viewsets, mixins
from coreapp.models import Tag
from coreapp.tags.serializers import TagModelSerializer
from coreapp.services.permissions import TagModelPermission


class TagViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset for instances of Tag model that provides `create()`, `destroy()` and `list()` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer
    permission_classes = [TagModelPermission]
