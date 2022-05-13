from django.contrib import admin

from family_budget_backend.budgets.models import Budget, Category
from family_budget_backend.users.admin import CreatedUpdatedAdmin


@admin.register(Budget)
class BudgetAdmin(CreatedUpdatedAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(CreatedUpdatedAdmin):
    pass
