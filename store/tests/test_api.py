import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Product, UserProductRelation, Category
from store.serializers import ProductSerializer, UserProductRelationSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Phone', slug='phones')
        self.product = Product.objects.create(title='iPhone 7', price=356, description='Super pooper',
                                              category=self.category, slug='iphone7', params={"asdf": 1})
        self.user = User.objects.create(username='testuser')

    def test_get(self):
        url = reverse('products-detail', args=(self.product.id,))
        response = self.client.get(url)
        response.data.pop('image', None)
        product_serializer_data = ProductSerializer(self.product).data
        product_serializer_data.pop('image', None)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(product_serializer_data, response.data)

    def test_create(self):
        url = reverse('products-list')
        data = {
            'title': 'iPhone 8',
            'price': '356.00',
            'slug': 'iphone8',
            'description': 'Super pooper',
            'params': {"asdf": 1},
            'category': self.category.id
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('products-detail', args=(self.product.id,))
        data = {
            'title': self.product.title,
            'price': '356.00',
            'description': 'Super pooper cool',
            'slug': 'iphone7'
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product.refresh_from_db()
        self.assertEqual('Super pooper cool', self.product.description)


class ProductCommentTestCase(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(title='iPhone 7', price=356, description='Super pooper')
        self.user = User.objects.create(username='test')
        self.userproductrelation = UserProductRelation.objects.create(user=self.user, product=self.product, rate=3, comment='Cool')

    def test_create(self):
        url = reverse('product_comment-list')
        data = {
            'user': self.user.id,
            'product': self.product.id,
            'rate': 3,
            'comment': 'Test comment',
            'advantages': 'Test +',
            'disadvantages': 'Test -'
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get(self):
        url = reverse('product_comment-detail', args=(self.userproductrelation.id,))
        response = self.client.get(url)
        user_product_relation_serializer_data = UserProductRelationSerializer(self.userproductrelation).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(user_product_relation_serializer_data, response.data)

