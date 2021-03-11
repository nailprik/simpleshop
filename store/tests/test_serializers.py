from django.test import TestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_ok(self):
        product1 = Product.objects.create(name='iPhone 7', price=356, params='Super pooper')
        product1_serializer_data = ProductSerializer(product1).data
        expected_data = {
            'id': product1.id,
            'name': 'iPhone 7',
            'price': '356.00',
            'params': 'Super pooper'
        }
        self.assertEqual(product1_serializer_data, expected_data)
