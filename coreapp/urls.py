from django.urls import path, include
from rest_framework import routers
from coreapp import views

app_name = "coreapp"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register (r'pages', views.PageViewSet)
router.register (r'tags', views.TagViewSet)
router.register (r'posts', views.PostViewSet)

urlpatterns = router.urls

