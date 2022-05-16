from django.db import models

from family_budget_backend.users.models import CreatedUpdated


class Transaction(CreatedUpdated):
    name = models.CharField(max_length=40)
    amount = models.IntegerField()
    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )

    class Meta(CreatedUpdated.Meta):
        ordering = ('category__name',)

    def __str__(self):
        return f'{self.name} - {self.amount} - {self.budget}'


class Budget(CreatedUpdated):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned'
    )
    viewers = models.ManyToManyField(
        'users.User',
        related_name='shared',
        blank=True
    )

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
