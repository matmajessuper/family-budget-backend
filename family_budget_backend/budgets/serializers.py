from django.db.models import Sum
from rest_framework import serializers

from family_budget_backend.budgets.models import Budget, Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'name', 'amount', 'budget', 'category')


class BudgetSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ('id', 'title', 'owner', 'viewers', 'balance', 'transactions')
        read_only_fields = ('owner',)

    @staticmethod
    def get_balance(obj):
        return obj.transactions.aggregate(Sum('amount')).get('amount__sum')
