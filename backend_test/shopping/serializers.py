from rest_framework import serializers

from .models import ShoppingList


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ["user", "title", "total_cost"]
