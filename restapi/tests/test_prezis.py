from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from restapi.models import Creator, Prezi
from restapi.tests.factories import PreziFactory, UserFactory


class TestPrezis(APITestCase):

    def setUp(self):
        # ensure database is clean before tests
        get_user_model().objects.all().delete()
        Creator.objects.all().delete()
        Prezi.objects.all().delete()

        # Prezi object at index 0 is older than Prezi object at index 1
        self.prezis = [
            PreziFactory(title='title1'),
            PreziFactory(title='title2', created_at=timezone.now())
        ]

    def test_get_prezis(self):
        url = reverse('prezis-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 2)

    def test_prezi_order(self):
        url = reverse('prezis-list')
        response = self.client.get(url, params={'order': 'DESC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(results[0]['title'], self.prezis[1].title)
        self.assertEqual(results[1]['title'], self.prezis[0].title)

        url = reverse('prezis-list')
        response = self.client.get(url, params={'order': 'ASC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(results[1]['title'], self.prezis[0].title)
        self.assertEqual(results[0]['title'], self.prezis[1].title)

    def test_get_prezi_by_id(self):
        url = reverse('prezis-detail', args=(self.prezis[0].id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.prezis[0].id))

    def test_searching_prezi_by_title(self):
        prezi = PreziFactory(title='I love prezi')

        url = reverse('prezis-list')
        response = self.client.get(url, {'search': 'prezi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], prezi.title)

        url = reverse('prezis-list')
        response = self.client.get(url, {'search': 'chicken'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 0)

    def test_authenticated_user_can_update_prezi(self):
        UserFactory(username='user1', password='password123')
        old_title = self.prezis[0].title
        new_title = 'new title'

        url = reverse('prezis-detail', args=(self.prezis[0].id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], old_title)

        # try to update instance without being unauthenticated
        response = self.client.patch(url, data={'title': new_title})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check that the instance has not been updated
        url = reverse('prezis-detail', args=(self.prezis[0].id,))
        response = self.client.get(url)
        self.assertEqual(response.data['title'], old_title)

        # try to update the instance with authenticated user
        self.client.login(username='user1', password='password123')
        response = self.client.patch(url, data={'title': new_title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)
