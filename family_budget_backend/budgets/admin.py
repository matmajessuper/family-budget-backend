from django.contrib import admin

from family_budget_backend.budgets.models import Budget, Category, Transaction
from family_budget_backend.users.admin import CreatedUpdatedAdmin


@admin.register(Transaction)
class TransactionAdmin(CreatedUpdatedAdmin):
    pass


class TransactionInline(admin.TabularInline):
    model = Transaction


@admin.register(Budget)
class BudgetAdmin(CreatedUpdatedAdmin):
    inlines = (TransactionInline,)


@admin.register(Category)
class CategoryAdmin(CreatedUpdatedAdmin):
    pass
