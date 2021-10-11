from django.test import TestCase

from .serializers import IngredientSerializer


class IngredientSerializerTest(TestCase):
    def test_serializes_valid_data(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "name": "My New Ingredient",
                "unit": "g",
                "cost_per_unit": 59.99,
            }
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 59.99,
        }

    def test_fails_if_name_missing(self):
        serializer = IngredientSerializer(
            data={
                "category": "fresh",
                "unit": "g",
                "cost_per_unit": 59.99,
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
            }
        )
        assert not serializer.is_valid()
