from rest_framework import viewsets, mixins
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer

