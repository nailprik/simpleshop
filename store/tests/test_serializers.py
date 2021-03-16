from django.test import TestCase

from store.models import Product, Category
from store.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Phone', slug='phones')
        self.product = Product.objects.create(title='iPhone 9', price=356, description='Super pooper',
                                              category=self.category, slug='iphone9', params={"asdf":1})

    def test_ok(self):
        product_serializer_data = ProductSerializer(self.product).data
        expected_data = {
            'id': self.product.id,
            'title': 'iPhone 9',
            'price': '356.00',
            'slug': 'iphone9',
            'image': '/static/default.jpg',
            'description': 'Super pooper',
            'params': {"asdf": 1},
            'category': self.category.id
        }
        self.assertEqual(product_serializer_data, expected_data)
