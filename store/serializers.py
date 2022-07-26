from django.db import transaction

from rest_framework import serializers


from store.models import Cart, CartItem, Customer, Order, OrderItem, Owner, Product, Review, Shop
from main.models import User
from pprint import pprint


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['product', 'shop', 'customer',
                  'description', 'date', ]


class CustomerSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'birth_date', 'reviews']


class SimpleCustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, object):
        return f'{object.user.first_name} {object.user.last_name}'

    class Meta:
        model = Customer
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'is_vendor']


class SimpleShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description']


class ShopSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price',
                  'stock', 'shop', 'slug', 'image_link', 'reviews']


class ProductCreateSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price',
                  'stock', 'shop', 'slug', 'image_link', 'reviews']


class OwnerSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Owner
        fields = '__all__'


class OwnerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = '__all__'


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_status',
                  'order_items', 'created_at', 'shop']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    def save(self, **kwargs):

        cart = self.context['cart']
        cart_items = CartItem.objects \
            .select_related('product') \
            .filter(cart=cart)
        if not cart_items:
            raise serializers.ValidationError('The cart is empty.')

        for item in cart_items:
            order_for_item = Order.objects.filter(
                order_status='Pending', customer=cart.customer).first()
            if order_for_item is None:
                order_for_item = Order.objects.create(
                    shop=item.product.shop, customer=cart.customer)

            OrderItem.objects.create(
                order=order_for_item, product=item.product, quantity=item.quantity)

        cart.is_checkout = True
        cart.save()
        return cart

    # def save(self, **kwargs):
    #     with transaction.atomic():
    #         cart_id = self.validated_data['cart_id']

    #         customer = Customer.objects.get(
    #             user_id=self.context['user_id'])
    #         order = Order.objects.create(customer=customer)

    #         cart_items = CartItem.objects \
    #             .select_related('product') \
    #             .filter(cart_id=cart_id)
    #         order_items = [
    #             OrderItem(
    #                 order=order,
    #                 product=item.product,
    #                 unit_price=item.product.unit_price,
    #                 quantity=item.quantity
    #             ) for item in cart_items
    #         ]
    #         OrderItem.objects.bulk_create(order_items)

    #         Cart.objects.filter(pk=cart_id).delete()

    #         order_created.send_robust(self.__class__, order=order)

    #         return order
