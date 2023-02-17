from django.urls import path, include
from rest_framework import routers
from coreapp import views

app_name = "coreapp"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register (r'pages', views.PageViewSet)
router.register (r'tags', views.TagViewSet)
router.register (r'posts', views.PostViewSet)

urlpatterns = [
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('refresh/', views.RefreshAPIView.as_view(), name ='refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name = 'logout'),
    path('', include(router.urls)),
    ]


