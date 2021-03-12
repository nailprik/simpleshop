from rest_framework import serializers

from store.models import Product, UserProductRelation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserProductRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('user', 'product', 'rate', 'comment', 'advantages', 'disadvantages')
