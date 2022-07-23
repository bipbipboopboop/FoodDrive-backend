
from django.http import HttpRequest

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from store.models import Cart, CartItem, Customer, Shop, Product
from store.serializers import SimpleProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class UpdateCartSerializer(serializers.Serializer):
    shop = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartView(viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartItemSerializer
        if self.request.method == 'POST':
            return UpdateCartSerializer
        return CartItemSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        cart = Cart.objects.filter(
            user__user_id=user_id, is_checkout=False).first()
        cart_items = CartItem.objects.filter(cart=cart)
        result = CartItemSerializer(cart_items, many=True).data
        return result

    @action(detail=False, methods=['get'], url_path=r'view')
    def view(self, request: HttpRequest, *args, **kwargs) -> Response:
        try:
            return Response(self.get_queryset(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                f"Unable to view cart items. {e}",
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], url_path=r'update')
    def update_item(self, request: HttpRequest, *args, **kwargs) -> Response:
        try:
            user_id = request.user.id
            shop_id = request.data.get('shop')
            product_id = request.data.get('product')
            quantity = request.data.get('quantity')

            cart = Cart.objects.filter(
                user__user_id=user_id, is_checkout=False).first()
            if cart is None or int(cart.shop.id) != int(shop_id):
                user = Customer.objects.get(user_id=user_id)
                shop = Shop.objects.get(id=shop_id)
                if cart:
                    cart.delete()
                cart = Cart.objects.create(
                    user=user, shop=shop, is_checkout=False)

            cart_item = CartItem.objects.filter(
                cart=cart,
                product__id=product_id
            ).first()

            if cart_item is None:
                product = Product.objects.get(id=product_id)
                cart_item = CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity)
            else:
                cart_item.quantity = quantity
                cart_item.save()

            result = CartItemSerializer(cart_item, many=False).data
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                f"Unable to update cart item. {e}",
                status=status.HTTP_404_NOT_FOUND
            )
