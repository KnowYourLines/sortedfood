from rest_framework import mixins, viewsets

from .models import ShoppingList
from .serializers import ShoppingListSerializer


class ShoppingViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    lookup_field = "title"

    pass
