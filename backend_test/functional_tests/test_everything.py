from http import HTTPStatus

from django.test import TransactionTestCase

from ingredient.models import Ingredient


class IngredientIntegrationTest(TransactionTestCase):
    def test_saves_new_ingredient(self):
        new_ingredient = {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 59.99,
            "available": True,
        }
        response = self.client.post("/ingredient/", new_ingredient, format="json")
        assert response.status_code == HTTPStatus.CREATED
        assert response.data == {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 59.99,
            "available": True,
        }
        saved_ingredient = Ingredient.objects.get(name="My New Ingredient")
        assert saved_ingredient.name == "My New Ingredient"

    def test_updates_ingredient_cost(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=True,
        )
        created_product.save()
        response = self.client.patch(
            "/ingredient/My New Ingredient/new_cost_per_unit/?price=60"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 60,
            "available": True,
        }
        saved_ingredient = Ingredient.objects.get(name="My New Ingredient")
        assert saved_ingredient.cost_per_unit == 60

    def test_mark_ingredient_unavailable(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=True,
        )
        created_product.save()
        response = self.client.patch("/ingredient/My New Ingredient/flag_unavailable/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "category": "fresh",
            "name": "My New Ingredient",
            "unit": "g",
            "cost_per_unit": 59.99,
            "available": False,
        }
        saved_ingredient = Ingredient.objects.get(name="My New Ingredient")
        assert not saved_ingredient.available
