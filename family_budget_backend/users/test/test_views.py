from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from family_budget_backend.users.test.factories import UserFactory


class TestBudgetTestCase(APITestCase):
    def test_users_list(self):
        url = reverse('users-list')
        user = UserFactory()
        UserFactory()
        UserFactory()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), get_user_model().objects.all().count())

    def test_users_filter(self):
        url = reverse('users-list')
        user = UserFactory()
        other_user = UserFactory(username='test_user')
        self.client.force_authenticate(user)
        response = self.client.get(url, {'username': 'test_user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data.get('results')[0].get('id'), str(other_user.id))
