from rest_framework import mixins, viewsets

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = "name"
    pass
