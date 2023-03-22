from coreapp.models import User
import pytest
from rest_framework.test import APIClient
import datetime
from tests.factories import UserFactory, PageFactory, PostFactory, TagFactory
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def image():
    image = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")
    return image


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
@pytest.fixture
def test_user():
    return User.objects.create_superuser(
        username="yulitta",
        email="test@example.com",
        password="user1234",
        first_name="Yulitta",
        last_name="Bekish"
    )


@pytest.fixture
def api_client_force_auth(test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.mark.django_db
@pytest.fixture
def test_user_1():
    return UserFactory()


@pytest.fixture
def api_client_1(test_user_1):
    client = APIClient()
    client.force_authenticate(test_user_1)
    return client


@pytest.mark.django_db
@pytest.fixture
def test_user_2():
    return UserFactory()


@pytest.fixture
def api_client_2(test_user_2):
    client = APIClient()
    client.force_authenticate(test_user_2)
    return client


@pytest.mark.django_db
@pytest.fixture
def test_user_3():
    return UserFactory()


@pytest.mark.django_db
@pytest.fixture
def test_tag_1():
    return TagFactory()


@pytest.mark.django_db
@pytest.fixture
def test_tag_2():
    return TagFactory()


@pytest.mark.django_db
@pytest.fixture
def test_tag_3():
    return TagFactory()


@pytest.mark.django_db
@pytest.fixture
def test_page_1(test_user_1, test_user):
    page = PageFactory(
        is_private=False,
        owner=test_user_1
    )
    page.followers.add(test_user)
    return page


@pytest.mark.django_db
@pytest.fixture
def test_page_2(test_user_2, test_user_1):
    page = PageFactory(
        is_private=True,
        owner=test_user_2
    )
    page.follow_requests.add(test_user_1)
    return page


@pytest.mark.django_db
@pytest.fixture
def test_page_3(test_user_2):
    return PageFactory(
        is_private=False,
        owner=test_user_2,
        unblock_date=datetime.datetime.max
    )


@pytest.mark.django_db
@pytest.fixture
def test_post_1(test_page_1):
    return PostFactory(
        page=test_page_1
    )


@pytest.mark.django_db
@pytest.fixture
def test_post_2(test_page_2):
    return PostFactory(
        page=test_page_2
    )
