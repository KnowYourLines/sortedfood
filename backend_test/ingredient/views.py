from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ingredient
from .serializers import IngredientSerializer, QueryParamSerializer


class IngredientViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = "name"

    @action(detail=True, methods=["patch"])
    def new_cost_per_unit(self, request, **kwargs):
        instance = self.get_object()
        query_params = QueryParamSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        ingredient = self.get_serializer(
            instance,
            data={"cost_per_unit": query_params.validated_data["price"]},
            partial=True,
        )
        ingredient.is_valid(raise_exception=True)
        ingredient.save()
        return Response(ingredient.validated_data)
