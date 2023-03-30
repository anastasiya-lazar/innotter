import pytest
from rest_framework import status
from django.urls import reverse
from coreapp.models import Tag


@pytest.mark.django_db
class TestTagModel:
    @pytest.mark.parametrize("idx", [0, 1])
    def test_create_tag(self, idx, api_client, api_client_force_auth):
        client, return_code = [
            (api_client, status.HTTP_403_FORBIDDEN),
            (api_client_force_auth, status.HTTP_201_CREATED),
        ][idx]
        payload = dict(name="tag2")
        response = client.post("/tags/", payload)
        assert response.status_code == return_code

    def test_get_tag_list(self, api_client, test_tag_1, test_tag_2):
        response = api_client.get("/tags/")
        assert response.status_code == status.HTTP_200_OK
        assert Tag.objects.count() == 2

    @pytest.mark.parametrize("idx", [0, 1])
    def test_delete_tag(self, idx, api_client, api_client_force_auth, test_tag_2):
        client, return_code = [
            (api_client, status.HTTP_403_FORBIDDEN),
            (api_client_force_auth, status.HTTP_204_NO_CONTENT),
        ][idx]
        response = client.delete(reverse("coreapp:tags-detail", args=(test_tag_2.id,)))
        assert response.status_code == return_code
