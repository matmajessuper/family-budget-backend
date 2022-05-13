from django.db import models
from django.contrib.postgres.fields import ArrayField

from family_budget_backend.users.models import CreatedUpdated


class Budget(CreatedUpdated):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned'
    )
    viewer = models.ManyToManyField('users.User', related_name='shared')
    category = models.ManyToManyField('Category', related_name='budgets')
    expenses = ArrayField(ArrayField(
        models.CharField(max_length=50),
        size=2
    ))
    incomes = ArrayField(ArrayField(
        models.CharField(max_length=50),
        size=2
    ))

    class Meta(CreatedUpdated.Meta):
        unique_together = ('owner', 'title')

    def __str__(self):
        return self.title


class Category(CreatedUpdated):
    name = models.CharField(max_length=50)

    class Meta(CreatedUpdated.Meta):
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
