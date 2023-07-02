from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category


class Review(models.Model):
    """
    This is the review model that references a product model
    and a user model as Foreign Keys
    It creates a review with a title, body, and creation date.
    It has two more fields, usused as of yet, for tracking if and
    when a review is edited. Which might be useful if other users
    were given the ability to interact with the given review.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(null=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    """
    This is the rating model. It ties a rating across the two models of
    user and product.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], default=0)

    def __str__(self):
        return f'{self.user.username} rated {self.product.name} \
            with {self.rating} stars'
