from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    params = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class UserProductRelation(models.Model):
    RATE_CHOICES = [
        (1, 'Awful'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    advantages = models.TextField(max_length=200, null=True)
    disadvantages = models.TextField(max_length=200, null=True)
    rate = models.SmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return self.user.username + ' rate ' + self.product.name
