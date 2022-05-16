from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from family_budget_backend.budgets.models import Budget, Category, Transaction
from family_budget_backend.budgets.serializers import BudgetSerializer, CategorySerializer, TransactionSerializer


class BudgetsViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):

    serializer_class = BudgetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('title',)

    def get_queryset(self):
        if self.action == 'shared':
            return Budget.objects.filter(viewers=self.request.user)
        return Budget.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['GET'])
    def shared(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TransactionsViewSet(GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(budget__owner=self.request.user)


class CategoriesViewSet(GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
