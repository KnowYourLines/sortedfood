from rest_framework import mixins, viewsets, permissions

from .models import ShoppingList
from .permissions import IsOwner
from .serializers import ShoppingListSerializer


class ShoppingViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    lookup_field = "title"
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pass
