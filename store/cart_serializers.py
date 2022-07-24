from rest_framework import serializers
from store.models import Cart, CartItem, Product
from store.serializers import CustomerSerializer, ShopSerializer, SimpleCustomerSerializer, SimpleShopSerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class UpdateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['cart_items']


class UpdateCartItemsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartSerializer(serializers.ModelSerializer):
    shop = SimpleShopSerializer()
    customer = SimpleCustomerSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'shop', 'customer', 'is_checkout']


class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['customer', 'shop', 'cart_items']


"""
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    customer = models.ForeignKey(
        Customer, related_name=CARTS_RELATED_NAME, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name=CARTS_RELATED_NAME, null=True)
    is_checkout = models.BooleanField(default=False)
"""
