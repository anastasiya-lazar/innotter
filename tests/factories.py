import factory
from coreapp.models import User, Page, Post, Tag


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = "user1234"
    email = factory.Faker("email")
    username = factory.Sequence(lambda n: "test%02d" % n)

    class Meta:
        model = User


class UserCreateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test4"
    email = "test4@example.com"
    password = "user1234"
    first_name = "test4"
    last_name = "test4"


class PageFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "test_page_%02d" % n)
    description = factory.Faker("sentence")

    class Meta:
        model = Page


class PageCreateFactory(factory.django.DjangoModelFactory):
    name = "string"
    description = "string"

    class Meta:
        model = Page


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "test_tag%02d" % n)

    class Meta:
        model = Tag


class PostFactory(factory.django.DjangoModelFactory):
    content = "string"

    class Meta:
        model = Post
