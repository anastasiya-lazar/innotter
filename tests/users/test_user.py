import pytest
from rest_framework import status
from django.urls import reverse
from coreapp.models import User, Page
from coreapp.services.auth_service import AuthService
from tests.factories import UserCreateFactory
import factory
from coreapp.services.exceptions import RefreshTokenException


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, api_client):
        payload = factory.build(dict, FACTORY_CLASS=UserCreateFactory)
        response = api_client.post("/users/", payload)
        data = response.data
        assert data["first_name"] == payload["first_name"]
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in data

    def test_get_user_list(self, api_client, test_user, test_user_1, test_user_2):
        response = api_client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) == 3

    def test_detail_user(self, api_client, test_user_1):
        response = api_client.get(reverse("coreapp:users-detail", args=(test_user_1.id,)))
        assert response.status_code == status.HTTP_200_OK

    def test_update_user(self, api_client_1, test_user_1):
        user = factory.build(dict, FACTORY_CLASS=UserCreateFactory)
        payload = dict(username=user["username"])
        response = api_client_1.patch(f"/users/{test_user_1.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == payload["username"]

    def test_delete_user_fail(self, api_client, test_user_1):
        response = api_client.delete(reverse("coreapp:users-detail", args=(test_user_1.id,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_success(self, api_client_1, test_user_1):
        response = api_client_1.delete(f"/users/{test_user_1.id}/")
        assert not User.objects.filter(id=test_user_1.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_login_user(self, api_client, test_user):
        payload = dict(email="test@example.com", password="user1234")
        response = api_client.post("/auth/login/", payload)
        data = response.data
        assert data["access_token"] and data["refresh_token"]
        assert response.status_code == status.HTTP_200_OK

    def test_invalid_refresh_token(self, api_client, test_user):
        payload = dict(refresh_token="invalid_token")
        api_client.post("/auth/refresh/", payload)
        assert RefreshTokenException

    def test_refresh_user(self, api_client, test_user):
        user_id = test_user.id
        refresh_token = AuthService().create_refresh_token(user_id)
        payload = dict(refresh_token=refresh_token)
        response = api_client.post("/auth/refresh/", payload)
        data = response.data
        assert data["access_token"] and data["refresh_token"]
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "role, expected_role, expected_staff_status, expected_superuser_status", [
            ("moderator", "moderator", True, False),
            ("admin", "admin", True, True),
            ("user", "user", False, False)
        ])
    def test_change_role(self, api_client_force_auth, test_user_1, role, expected_role, expected_staff_status,
                         expected_superuser_status):
        payload = dict(role=role)
        api_client_force_auth.patch(f"/users/{test_user_1.id}/change_user_role/", payload)
        user = User.objects.filter(id=test_user_1.id).first()
        assert user.role == expected_role
        assert user.is_staff == expected_staff_status
        assert user.is_superuser == expected_superuser_status

    def test_block_user(self, api_client_force_auth, test_user_1, test_page_1):
        payload = dict(is_blocked=True)
        api_client_force_auth.patch(f"/users/{test_user_1.id}/block_user/", payload)
        assert User.objects.filter(id=test_user_1.id).first().is_blocked
        assert Page.objects.filter(owner=test_user_1.id).first().unblock_date

    def test_unblock_user(self, api_client_force_auth, test_user_1, test_page_1):
        payload = dict(is_blocked=False)
        api_client_force_auth.patch(f"/users/{test_user_1.id}/block_user/", payload)
        assert not User.objects.filter(id=test_user_1.id).first().is_blocked
        if test_user_1.pages:
            assert not Page.objects.filter(owner=test_user_1.id).first().unblock_date

    def test_list_liked_posts(self, api_client_1, test_user_1):
        response = api_client_1.get(f"/users/{test_user_1.id}/list_of_liked_posts/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["liked"] == []
