from rest_framework import serializers
from store.cart_serializers import CartItemSerializer
import environ

env = environ.Env()


class ProductDataSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        product = self.context['product']
        return product['title']


class PriceDataSerializer(serializers.Serializer):
    currency = serializers.CharField(default="sgd")
    product_data = serializers.SerializerMethodField()
    unit_amount = serializers.SerializerMethodField()

    def get_product_data(self, obj):
        serializer = ProductDataSerializer(
            data=obj, context={'product': self.context['product']}
        )
        serializer.is_valid()
        return serializer.data

    def get_unit_amount(self, obj):
        product = self.context['product']
        return int(product['unit_price'] * 100)


class LineItemSerializer(serializers.Serializer):

    quantity = serializers.SerializerMethodField()
    price_data = serializers.SerializerMethodField()

    def get_price_data(self, obj):
        price_date_serializer = PriceDataSerializer(
            data=obj, context={'product': self.context['cart_item']['product']}
        )
        price_date_serializer.is_valid()
        return price_date_serializer.data

    def get_quantity(self, obj):
        return self.context['cart_item']['quantity']


class CreatePaymentSerializer(serializers.Serializer):

    def to_representation(self, instance):
        payment = super().to_representation(instance)

        cart_item_serializer = CartItemSerializer(
            many=True,
            data=self.context['cart_items']
        )

        cart_item_serializer.is_valid()
        cart_items = cart_item_serializer.data

        line_items = []

        if cart_items:
            for item in cart_items:
                line_item_serializer = LineItemSerializer(
                    data=item, context={'cart_item': item}
                )
                line_item_serializer.is_valid()
                line_items.append(line_item_serializer.data)
            payment["payment_method_types"] = ["card"]
            payment["mode"] = "payment"
            payment["line_items"] = line_items
            payment["success_url"] = env('PAYMENT_SUCCESS_URL')
            payment["cancel_url"] = env('PAYMENT_FAILURE_URL')

        return payment


"""
1) Add Items to Cart
2) Click Order
3) Pay
    PaymentView
        Iterate through the cart
        

"""
