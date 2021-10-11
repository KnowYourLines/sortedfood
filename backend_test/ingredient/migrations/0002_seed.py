import json

from django.db import migrations


def load_ingredients(apps, schema_editor):
    with open("data/ingredients.json") as json_file:
        ingredients = json.load(json_file)
        Ingredient = apps.get_model("ingredient", "Ingredient")
        initial_ingredients = []
        for ingredient in ingredients:
            try:
                cost_per_unit = float(ingredient["Cost Per Unit"])
            except ValueError:
                cost_per_unit = None
            initial_ingredients.append(
                Ingredient(
                    name=ingredient["Ingredient"],
                    category=ingredient["Excel Category"],
                    unit=ingredient["Unit"],
                    cost_per_unit=cost_per_unit,
                    available=True,
                )
            )
        Ingredient.objects.bulk_create(initial_ingredients)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingredient", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_ingredients),
    ]
