import datetime
import pytest
from rest_framework import status
from django.urls import reverse
from coreapp.models import Page
from rest_framework.test import APIClient
from tests.factories import PageCreateFactory
import factory

testdata = [("True", 1), ("False", 0)]


@pytest.mark.django_db
class TestPageModel:
    def test_create_page_fail(self, api_client, test_user_1):
        payload = factory.build(dict, FACTORY_CLASS=PageCreateFactory)
        response = api_client.post("/pages/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_page_success(self, api_client_force_auth, test_user_1):
        payload = factory.build(dict, FACTORY_CLASS=PageCreateFactory)
        response = api_client_force_auth.post("/pages/", payload)
        page = Page.objects.filter(id=response.data["id"]).first()
        assert response.data["name"] == page.name
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_page_list(self, api_client, test_page_1, test_page_2, test_page_3):
        response = api_client.get("/pages/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_detail_page_success(self, api_client, test_page_1):
        response = api_client.get(reverse("coreapp:pages-detail", args=(test_page_1.id,)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == Page.objects.filter(id=test_page_1.id).first().name

    def test_detail_page_fail(self, api_client, test_page_3):
        response = api_client.get(reverse("coreapp:pages-detail", args=(test_page_3.id,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_page_success(self, api_client_1, test_page_1):
        payload = factory.build(dict, FACTORY_CLASS=PageCreateFactory)
        response = api_client_1.patch(f"/pages/{test_page_1.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == payload["name"]

    def test_update_page_fail(self, api_client_1, test_user_2, test_page_1):
        payload = dict(owner=test_user_2)
        api_client_1.patch(f"/pages/{test_page_1.id}/", payload)
        assert KeyError

    @pytest.mark.parametrize("idx", [0, 1])
    def test_delete_page(self, idx, api_client_1, api_client_force_auth, test_page_1):
        client, return_code = [
            (api_client_1, status.HTTP_204_NO_CONTENT),
            (api_client_force_auth, status.HTTP_403_FORBIDDEN),
        ][idx]
        response = client.delete(reverse("coreapp:pages-detail", args=(test_page_1.id,)))
        assert response.status_code == return_code

    def test_block_page(self, api_client_force_auth, test_page_2):
        payload = dict(unblock_date=datetime.datetime.now() + datetime.timedelta(weeks=2))
        response = api_client_force_auth.patch(f"/pages/{test_page_2.id}/block_page/", payload)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("value,expected_count", testdata)
    def test_follow_unfollow_public_page(self, api_client_2, test_page_1, value, expected_count):
        payload = dict(follow=value)
        response = api_client_2.patch(f"/pages/{test_page_1.id}/follow_and_unfollow_page/", payload)
        page = Page.objects.filter(id=response.data["id"]).first()
        assert page.followers.count() == expected_count

    @pytest.mark.parametrize("value,expected_count", [("True", 2), ("False", 1)])
    def test_follow_unfollow_private_page(self, test_user_3, test_page_2, value, expected_count):
        client = APIClient()
        client.force_authenticate(user=test_user_3)
        payload = dict(follow=value)
        response = client.patch(f"/pages/{test_page_2.id}/follow_and_unfollow_page/", payload)
        page = Page.objects.filter(id=response.data["id"]).first()
        assert page.follow_requests.count() == expected_count

    def test_follow_page_fail(self, api_client_1, test_page_3):
        payload = dict(follow=True)
        response = api_client_1.patch(f"/pages/{test_page_3.id}/follow_and_unfollow_page/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list_follow_requests(self, api_client_2, test_page_2):
        api_client_2.get(f"/pages/{test_page_2.id}/get_list_follow_requests/")
        page = Page.objects.filter(id=test_page_2.id).first()
        assert page.follow_requests.count() == 1

    @pytest.mark.parametrize("accept,expected_result", testdata)
    def test_accept_or_decline_all_follow_requests(self, test_page_2, api_client_2, accept, expected_result):
        payload = dict(accept=accept)
        api_client_2.patch(f"/pages/{test_page_2.id}/accept_or_decline_follow_requests/", payload)
        page = Page.objects.filter(id=test_page_2.id).first()
        assert page.follow_requests.count() == 0
        assert page.followers.count() == expected_result

    @pytest.mark.parametrize("accept,expected_result", testdata)
    def test_accept_or_decline_one_follow_request(
            self, test_page_2, test_user_1,
            api_client_2, accept, expected_result
    ):
        payload = dict(accept=accept, user_id=test_user_1.id)
        api_client_2.patch(f"/pages/{test_page_2.id}/accept_or_decline_follow_requests/", payload)
        page = Page.objects.filter(id=test_page_2.id).first()
        assert page.follow_requests.count() == 0
        assert page.followers.count() == expected_result
