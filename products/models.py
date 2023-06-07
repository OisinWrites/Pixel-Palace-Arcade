from django.db import models
from django.db.models import Avg
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    """
    Model for product. Products are created with
    a defined category, price, name, image, and description.
    The aggregate rating is filled and updated everytime the model is
    called upon, using all existing rating models' values at the given
    time.
    """
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_variants = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    aggregaterating = models.DecimalField(max_digits=6, decimal_places=2,
                                          null=True, blank=True)
    reviewed = models.BooleanField(default=False, null=True, blank=True)
    image_url = models.URLField(max_length=1824, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def calculate_average_rating(self):
        average_rating = self.rating_set.aggregate(
            average_rating=Avg('rating'))['average_rating']
        if average_rating is not None:
            return Decimal(average_rating).quantize(Decimal('0.0'))
        return None

    @property
    def aggregaterating(self):
        return self.calculate_average_rating()

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
