from rest_framework import serializers

from family_budget_backend.budgets.models import Budget, Category


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'title', 'owner', 'viewers', 'category', 'expenses', 'incomes')
        read_only_fields = ('owner',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
