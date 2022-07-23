from rest_framework import serializers
from store.models import Cart, CartItem, Product


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class UpdateCartSerializer(serializers.Serializer):
    shop = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
