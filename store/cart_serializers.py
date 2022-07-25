from rest_framework import serializers
from store.models import Cart, CartItem, Product
from store.serializers import SimpleCustomerSerializer, SimpleShopSerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class UpdateCartItemsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        product = Product.objects.get(
            pk=validated_data.get('product_id'))
        cart = Cart.objects.get(pk=validated_data.get('cart_id'))
        cart_item = CartItem.objects.filter(
            cart=cart, product=product)
        quantity = validated_data.get('quantity')
        if cart_item.exists():
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity)
        # print('cart', cart)
        return cart


class SimpleCartSerializer(serializers.ModelSerializer):
    shop = SimpleShopSerializer()
    customer = SimpleCustomerSerializer()
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'shop',
                  'customer', 'is_checkout', 'cart_items']


class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['customer', 'shop']
