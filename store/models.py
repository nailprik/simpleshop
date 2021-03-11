from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    params = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'
