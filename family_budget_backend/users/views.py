from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from .serializers import UserSerializer


class UsersViewSet(GenericViewSet,
                  mixins.ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('username',)
