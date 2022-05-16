import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

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
    title = factory.Sequence(lambda n: f'budget{n}')


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = 'budgets.Transaction'

    id = factory.Faker('uuid4')
    budget = factory.SubFactory(BudgetFactory)
    name = factory.Sequence(lambda n: f'transaction{n}')
    amount = FuzzyInteger(-10000, 10000)
