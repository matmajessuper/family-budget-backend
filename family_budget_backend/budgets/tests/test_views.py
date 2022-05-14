import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from family_budget_backend.budgets.models import Budget, Category
from family_budget_backend.budgets.tests.factories import BudgetFactory, CategoryFactory
from family_budget_backend.users.test.factories import UserFactory


class TestBudgetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_create_success(self):
        url = reverse('budgets-list')
        payload = {
            'title': 'budget',
            'expenses': [
                ['water', '-200']
            ],
            'incomes': [
                ['salary', '1000']
            ]
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Budget.objects.filter(title=payload.get('title'), owner=self.user).exists())

    def test_list_only_owned(self):
        BudgetFactory()
        BudgetFactory(owner=self.user)
        url = reverse('budgets-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Budget.objects.all().count(), 2)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_update_success(self):
        budget = BudgetFactory(owner=self.user)
        url = reverse('budgets-detail', kwargs={'pk': str(budget.id)})
        payload = {
            'expenses': [
                ['water', '-200']
            ],
            'incomes': [
                ['salary', '1000']
            ]
        }
        self.assertNotEqual(budget.expenses, payload.get('expenses'))
        self.assertNotEqual(budget.incomes, payload.get('incomes'))
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertEqual(budget.expenses, payload.get('expenses'))
        self.assertEqual(budget.incomes, payload.get('incomes'))

    def test_delete_success(self):
        budget = BudgetFactory(owner=self.user)
        url = reverse('budgets-detail', kwargs={'pk': str(budget.id)})
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Budget.objects.filter(id=budget.id).exists())

    def test_shared(self):
        budget = BudgetFactory()
        budget.viewers.add(self.user)
        url = reverse('budgets-shared')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_update_category(self):
        budget = BudgetFactory(owner=self.user)
        category = CategoryFactory()
        url = reverse('budgets-detail', kwargs={'pk': str(budget.id)})
        payload = {
            'category': [str(category.id)]
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertTrue(budget.category.filter(id=category.id).exists())


class TestCategoryTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.url = reverse('categories-list')

    def test_create_success(self):
        payload = {
            'name': 'category'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        CategoryFactory()
        CategoryFactory()
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), Category.objects.all().count())
