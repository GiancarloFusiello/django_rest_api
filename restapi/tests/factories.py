import uuid
from datetime import datetime

import factory
import pytz
from django.conf import settings

from restapi.models import Creator, Prezi


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'p@ssw0rd')

    is_superuser = True
    is_staff = True
    is_active = True

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)


class CreatorFactory(factory.django.DjangoModelFactory):
    id = uuid.uuid4()
    name = factory.Sequence(lambda n: 'creator%d' % n)

    class Meta:
        model = Creator
        django_get_or_create = ('id',)


class PreziFactory(factory.django.DjangoModelFactory):
    picture = factory.Sequence(lambda n: 'http://placeholder.it/%d' % n)
    title = factory.Sequence(lambda n: 'title%d' % n)
    created_at = datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE))
    creator = factory.SubFactory(CreatorFactory)

    class Meta:
        model = Prezi


