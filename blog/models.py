from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    aggregate_rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_rating = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - \
             {self.user_rating}'
