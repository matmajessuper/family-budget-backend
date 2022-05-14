import random

import factory
from factory.django import DjangoModelFactory

from family_budget_backend.users.test.factories import UserFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'budgets.Category'

    name = factory.Sequence(lambda n: f'category{n}')


class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = 'budgets.Budget'

    id = factory.Faker('uuid4')
    owner = factory.SubFactory(UserFactory)
    expenses = factory.Sequence(lambda n: [f'expense {n}', random.randint(1, 1000)])
    incomes = factory.Sequence(lambda n: [f'income {n}', random.randint(1, 1000)])
