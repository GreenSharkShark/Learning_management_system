from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwnerOrReadOnly
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
