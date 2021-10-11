from django.db import models
from django.utils.translation import ugettext_lazy as _


CATEGORIES = (("fresh", "fresh"), ("staple", "staple"))
UNITS = (("g", "g"), ("ml", "ml"), ("tsp", "tsp"), ("tbsp", "tbsp"))


class Ingredient(models.Model):
    name = models.CharField(_("Ingredient"), max_length=250)

    category = models.CharField(choices=CATEGORIES, max_length=64)

    unit = models.CharField(choices=UNITS, max_length=64)

    cost_per_unit = models.FloatField(_("Cost Per Unit"), null=True, blank=True)

    available = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
