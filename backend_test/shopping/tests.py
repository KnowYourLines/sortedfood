from django.test import TestCase

from .serializers import ShoppingListSerializer


class ShoppingListSerializerTest(TestCase):
    fixtures = ["shopping/shopping_test_fixture.json"]

    def test_serializes_valid_data(self):
        serializer = ShoppingListSerializer(
            data={
                "user": 1,
                "title": "My Shopping List",
            }
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.data == {
            "user": 1,
            "title": "My Shopping List",
        }

    def test_fails_if_data_invalid(self):
        serializer = ShoppingListSerializer(
            data={
                "user": 111111111111,
                "title": "My Shopping List",
            }
        )
        assert not serializer.is_valid()
