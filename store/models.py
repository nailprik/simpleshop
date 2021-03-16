from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, verbose_name='Цена', decimal_places=2)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение', default='static/default.jpg')
    description = models.TextField(verbose_name='Описание', null=True)
    params = models.JSONField(verbose_name='Параметры', blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


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


class CartProduct(models.Model):
    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=8, verbose_name='Общая цена', decimal_places=2)

    def __str__(self):
        return f"Товар: {self.product.title} (для корзины)"


class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=8, verbose_name='Общая цена', decimal_places=2)

    def __str__(self):
        return self.id


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'Покупатель {self.user.first_name} {self.user.last_name}'
