from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from ingredient.models import Ingredient
from rest_framework.exceptions import ValidationError

from shopping.models import ShoppingList, ShoppingListItem


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


class ShoppingListIntegrationTest(TransactionTestCase):
    def test_finds_latest_shopping_list_total_cost_of_available_items_only(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=True,
        )
        created_product.save()
        created_product2 = Ingredient(
            category="fresh",
            name="My New Ingredient 2",
            unit="g",
            cost_per_unit=10,
            available=True,
        )
        created_product2.save()
        user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        created_shopping_list = ShoppingList(user=user, title="My Shopping List")
        created_shopping_list.save()
        created_shopping_list_item = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product, quantity=1
        )
        created_shopping_list_item.save()
        created_shopping_list_item2 = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product2, quantity=1
        )
        created_shopping_list_item2.save()
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/shopping/My Shopping List/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "user": user.id,
            "title": "My Shopping List",
            "total_cost": 69.99,
        }

        created_product3 = Ingredient(
            category="fresh",
            name="My New Ingredient 3",
            unit="g",
            cost_per_unit=10,
            available=True,
        )
        created_product3.save()
        created_shopping_list_item3 = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product3, quantity=1
        )
        created_shopping_list_item3.save()

        response = self.client.get("/shopping/My Shopping List/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "user": user.id,
            "title": "My Shopping List",
            "total_cost": 79.99,
        }

        created_product3.available = False
        created_product3.save()

        response = self.client.get("/shopping/My Shopping List/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "user": user.id,
            "title": "My Shopping List",
            "total_cost": 69.99,
        }

    def test_must_be_shopping_list_owner(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=True,
        )
        created_product.save()
        created_product2 = Ingredient(
            category="fresh",
            name="My New Ingredient 2",
            unit="g",
            cost_per_unit=10,
            available=True,
        )
        created_product2.save()
        user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )

        created_shopping_list = ShoppingList(user=user, title="My Shopping List")
        created_shopping_list.save()
        created_shopping_list_item = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product, quantity=1
        )
        created_shopping_list_item.save()
        created_shopping_list_item2 = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product2, quantity=1
        )
        created_shopping_list_item2.save()
        get_user_model().objects.create_user(username="testuser2", password="123456")
        self.client.login(username="testuser2", password="123456")
        response = self.client.get("/shopping/My Shopping List/")
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_ingredient_remains_on_shopping_list_when_made_unavailable(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=True,
        )
        created_product.save()
        user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        created_shopping_list = ShoppingList(user=user, title="My Shopping List")
        created_shopping_list.save()
        created_shopping_list_item = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product, quantity=1
        )
        created_shopping_list_item.save()
        created_product.available = False
        created_product.save()
        assert created_shopping_list.items.all()[0] == created_shopping_list_item

    def test_unavailable_ingredient_cannot_be_added_to_shopping_list(self):
        created_product = Ingredient(
            category="fresh",
            name="My New Ingredient",
            unit="g",
            cost_per_unit=59.99,
            available=False,
        )
        created_product.save()
        user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        created_shopping_list = ShoppingList(user=user, title="My Shopping List")
        created_shopping_list.save()
        created_shopping_list_item = ShoppingListItem(
            shopping_list=created_shopping_list, ingredient=created_product, quantity=1
        )
        with self.assertRaises(ValidationError) as error:
            created_shopping_list_item.save()
        assert (
            str(error.exception)
            == "[ErrorDetail(string='Ingredient is unavailable', code='invalid')]"
        )
