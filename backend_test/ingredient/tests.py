from django.test import TestCase

from .serializers import IngredientSerializer, QueryParamSerializer


class IngredientSerializerTest(TestCase):
    def test_serializes_valid_data(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "name": "My New Ingredient",
                "unit": "g",
                "cost_per_unit": 59.99,
                "available": True,
            }
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 59.99,
            "available": True,
        }

    def test_fails_if_name_missing(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "unit": "g",
                "cost_per_unit": 59.99,
                "available": True,
            }
        )
        assert not serializer.is_valid()

    def test_fails_if_category_invalid(self):
        serializer = IngredientSerializer(
            data={
                "category": "not a real category",
                "name": "My New Ingredient",
                "unit": "g",
                "cost_per_unit": 59.99,
                "available": True,
            }
        )
        assert not serializer.is_valid()

    def test_fails_if_unit_invalid(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "name": "My New Ingredient",
                "unit": "a ton",
                "cost_per_unit": 59.99,
                "available": True,
            }
        )
        assert not serializer.is_valid()

    def test_fails_if_cost_invalid(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "name": "My New Ingredient",
                "unit": "g",
                "cost_per_unit": "abc",
                "available": True,
            }
        )
        assert not serializer.is_valid()

    def test_fails_if_availability_invalid(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "name": "My New Ingredient",
                "unit": "g",
                "cost_per_unit": "abc",
                "available": 2,
            }
        )
        assert not serializer.is_valid()


class QueryParamSerializerTest(TestCase):
    def test_serializes_valid_data(self):
        serializer = QueryParamSerializer(data={"price": 5})
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {"price": 5}

    def test_fails_if_data_invalid(self):
        serializer = QueryParamSerializer(data={"price": "abc"})
        assert not serializer.is_valid()
