from django.urls import path, include
from rest_framework import routers
from coreapp.users.views import UserViewSet, AuthenticationViewSet
from coreapp.pages.views import PageViewSet
from coreapp.posts.views import PostViewSet
from coreapp.tags.views import TagViewSet

app_name = "coreapp"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"pages", PageViewSet, basename="pages")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"auth", AuthenticationViewSet, basename="auth")

urlpatterns = router.urls
