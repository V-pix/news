import pytest
from posts.models import Chanel, Post


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567')


@pytest.fixture
def channel(user):
    return Chanel.objects.create(title='Test channel', author=user)


@pytest.fixture
def post(channel, user):
   return Post.objects.create(text='Test text', chanel=channel, author=user)