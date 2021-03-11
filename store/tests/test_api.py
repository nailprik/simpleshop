import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name='iPhone 7', price=356, params='Super pooper')

    def test_get(self):
        url = reverse('products-list')
        response = self.client.get(url)
        product1_serializer_data = ProductSerializer([self.product1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(product1_serializer_data, response.data)

    def test_create(self):
        url = reverse('products-list')
        data = {
            'name': 'iPhone 8',
            'price': '500',
            'params': 'Super pooper'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {
            'name': self.product1.name,
            'price': '356.00',
            'params': 'Super pooper cool'
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product1.refresh_from_db()
        self.assertEqual('Super pooper cool', self.product1.params)