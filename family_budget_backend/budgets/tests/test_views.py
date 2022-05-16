import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from family_budget_backend.budgets.models import Budget, Category, Transaction
from family_budget_backend.budgets.tests.factories import BudgetFactory, CategoryFactory, TransactionFactory
from family_budget_backend.users.test.factories import UserFactory


class TestBudgetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_create_success(self):
        url = reverse('budgets-list')
        payload = {
            'title': 'budget'
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
            'title': 'changed'
        }
        self.assertNotEqual(budget.title, payload.get('title'))
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertEqual(budget.title, payload.get('title'))

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

    def test_transaction_order(self):
        url = reverse('budgets-list')
        budget = BudgetFactory(owner=self.user)
        category_family = CategoryFactory(name='family')
        category_work = CategoryFactory(name='work')
        t1 = TransactionFactory(budget=budget, category=category_family)
        t2 = TransactionFactory(budget=budget, category=category_family)
        t3 = TransactionFactory(budget=budget, category=category_work)
        t4 = TransactionFactory(budget=budget)
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        transactions = response.data.get('results')[0].get('transactions')
        self.assertEqual(transactions[0].get('id'), str(t1.id))
        self.assertEqual(transactions[1].get('id'), str(t2.id))
        self.assertEqual(transactions[2].get('id'), str(t3.id))
        self.assertEqual(transactions[3].get('id'), str(t4.id))

    def test_filter(self):
        BudgetFactory(owner=self.user)
        budget = BudgetFactory(owner=self.user)
        url = reverse('budgets-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url, {'title': budget.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data.get('results')[0].get('id'), str(budget.id))

    def test_share_with_user(self):
        budget = BudgetFactory(owner=self.user)
        other_user = UserFactory()
        url = reverse('budgets-detail', kwargs={'pk': str(budget.id)})
        payload = {
            'viewers': [str(other_user.id)]
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertEqual(str(budget.viewers.first().id), other_user.id)

    def test_pagination(self):
        for _ in range(20):
            BudgetFactory(owner=self.user)
        url = reverse('budgets-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 20)
        self.assertEqual(len(response.data.get('results')), 10)
        next_page = response.data.get('next')
        response = self.client.get(next_page)
        self.assertEqual(len(response.data.get('results')), 10)

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


class TestTransactionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_create_success(self):
        url = reverse('transactions-list')
        budget = BudgetFactory()
        payload = {
            'name': 'expense',
            'amount': 2345,
            'budget': str(budget.id)
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_success(self):
        budget = BudgetFactory(owner=self.user)
        transaction = TransactionFactory(budget=budget)
        url = reverse('transactions-detail', kwargs={'pk': str(transaction.id)})
        payload = {
            'name': 'expense',
            'amount': 2345,
        }
        self.client.force_authenticate(self.user)
        self.assertNotEqual(transaction.name, payload.get('name'))
        response = self.client.patch(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.name, payload.get('name'))

    def test_delete_success(self):
        budget = BudgetFactory(owner=self.user)
        transaction = TransactionFactory(budget=budget)
        url = reverse('transactions-detail', kwargs={'pk': str(transaction.id)})
        self.client.force_authenticate(self.user)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(id=transaction.id).exists())

    def test_update_category_success(self):
        budget = BudgetFactory(owner=self.user)
        transaction = TransactionFactory(budget=budget)
        category = CategoryFactory()
        url = reverse('transactions-detail', kwargs={'pk': str(transaction.id)})
        payload = {
            'category': str(category.id)
        }
        self.client.force_authenticate(self.user)
        self.client.patch(url, json.dumps(payload), content_type='application/json')
        transaction.refresh_from_db()
        self.assertEqual(transaction.category, category)
