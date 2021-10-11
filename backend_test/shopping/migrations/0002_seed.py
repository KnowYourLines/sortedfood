import json
import uuid

from django.contrib.auth import get_user_model
from django.db import migrations


def load_shopping_lists(apps, schema_editor):
    with open("data/shopping_lists.json") as json_file:
        shopping_list_items = json.load(json_file)
        ShoppingListItem = apps.get_model("shopping", "ShoppingListItem")
        ShoppingList = apps.get_model("shopping", "ShoppingList")
        Ingredient = apps.get_model("ingredient", "Ingredient")
        User = get_user_model()
        initial_items = []
        for item in shopping_list_items:

            shopping_list, created = ShoppingList.objects.get_or_create(
                title=item["Shopping List"],
                user_id=User.objects.create_user(username=uuid.uuid4()).id,
            )
            ingredient, created = Ingredient.objects.get_or_create(
                name=item["Ingredient"], available=True
            )
            initial_items.append(
                ShoppingListItem(
                    quantity=item["Amount"],
                    ingredient=ingredient,
                    shopping_list=shopping_list,
                )
            )

        ShoppingListItem.objects.bulk_create(initial_items)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shopping", "0001_initial"),
        ("ingredient", "0002_seed"),
    ]

    operations = [
        migrations.RunPython(load_shopping_lists),
    ]
