from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from family_budget_backend.budgets.models import Budget, Category
from family_budget_backend.budgets.serializers import BudgetSerializer, CategorySerializer


class BudgetsViewSet(GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    serializer_class = BudgetSerializer

    def get_queryset(self):
        if self.action == 'shared':
            return Budget.objects.filter(viewers=self.request.user)
        return Budget.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['GET'])
    def shared(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoriesViewSet(GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
