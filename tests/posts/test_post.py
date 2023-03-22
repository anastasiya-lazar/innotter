import pytest
from rest_framework import status
from django.urls import reverse
from coreapp.models import Post
from unittest.mock import patch
from coreapp.services.aws_ses_service import SESService


@pytest.mark.django_db
class TestPostModel:
    @patch.object(SESService, "send_email")
    @pytest.mark.parametrize("idx", [0, 1])
    def test_create_post(self, mock_object, idx, api_client, api_client_1, test_page_1):
        client, return_code = [
            (api_client, status.HTTP_403_FORBIDDEN),
            (api_client_1, status.HTTP_201_CREATED),
        ][idx]
        payload = dict(content="string1", page=test_page_1.id)
        response = client.post("/posts/", payload)
        assert response.status_code == return_code

    def test_get_post_list(self, api_client, test_post_1, test_post_2):
        response = api_client.get("/posts/")
        assert response.status_code == status.HTTP_200_OK
        assert Post.objects.count() == 2

    def test_detail_post(self, api_client, test_post_1):
        response = api_client.get(reverse("coreapp:posts-detail", args=(test_post_1.id,)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == Post.objects.filter(id=test_post_1.id).first().content

    def test_update_post(self, api_client_2, test_post_2):
        payload = dict(content="string1234")
        response = api_client_2.patch(f"/posts/{test_post_2.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == payload["content"]

    @pytest.mark.parametrize("to_like, expected_count", [("True", 1), ("False", 0)])
    def test_like_post(self, api_client_force_auth, test_post_2, to_like, expected_count):
        payload = dict(to_like=to_like)
        response = api_client_force_auth.patch(f"/posts/{test_post_2.id}/like_and_unlike_post/", payload)
        assert response.status_code == status.HTTP_200_OK
        post = Post.objects.filter(id=test_post_2.id).first()
        assert post.likes.count() == expected_count

    def test_delete_post(self, api_client_force_auth, test_post_2):
        response = api_client_force_auth.delete(reverse("coreapp:posts-detail", args=(test_post_2.id,)))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_news_feed(self, api_client_force_auth, test_page_1, test_post_1):
        response = api_client_force_auth.get("/posts/news_feed/")
        assert len(response.data) == 1
