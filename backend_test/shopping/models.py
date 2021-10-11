from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ingredient.models import Ingredient


class ShoppingList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(_("Title"), max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Shopping List")
        verbose_name_plural = _("Shopping Lists")

    @property
    def total_cost(self):
        # Calculate the total cost of the shopping list
        return 1


class ShoppingListItem(models.Model):

    shopping_list = models.ForeignKey(
        ShoppingList,
        verbose_name=_("Shopping List"),
        related_name="items",
        on_delete=models.CASCADE,
    )

    ingredient = models.ForeignKey(
        Ingredient, verbose_name=_("Ingredient"), on_delete=models.SET_NULL, null=True
    )

    quantity = models.FloatField(_("Quantity"))

    def __str__(self):
        return "{}: {}".format(self.shopping_list, self.ingredient)

    class Meta:
        verbose_name = _("Shopping List Item")
        verbose_name_plural = _("Shopping List Items")
