
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin

from rest_framework.response import Response
from rest_framework.decorators import action
from main.models import User

from store.models import Cart, CartItem, Customer, Shop, Product
from store.cart_serializers import CartSerializer, SimpleCartSerializer, CreateCartSerializer, UpdateCartItemsSerializer


# class CartView(viewsets.GenericViewSet):
#     # serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         print(self.request.method)
#         if self.request.method == 'POST':
#             return UpdateCartSerializer

#     def get_queryset(self):
#         user_id = self.request.user.id
#         cart = Cart.objects.filter(
#             user__user_id=user_id, is_checkout=False).first()
#         cart_items = CartItem.objects.filter(cart=cart)
#         result = CartItemSerializer(cart_items, many=True).data
#         return result

#     @action(detail=False, methods=['get'], url_path=r'view')
#     def view_cart(self, request: HttpRequest, *args, **kwargs) -> Response:
#         try:
#             return Response(data=self.get_queryset(), status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 f"Unable to view cart items. {e}",
#                 status=status.HTTP_404_NOT_FOUND
#             )

#     @action(detail=False, methods=['post'], url_path=r'update')
#     def update_item(self, request: HttpRequest, *args, **kwargs) -> Response:
#         try:
#             user_id = request.user.id
#             shop_id = request.data.get('shop')
#             product_id = request.data.get('product')
#             quantity = request.data.get('quantity')

#             cart = Cart.objects.filter(
#                 user__user_id=user_id, is_checkout=False).first()
#             if cart is None or int(cart.shop.id) != int(shop_id):
#                 user = Customer.objects.get(user_id=user_id)
#                 shop = Shop.objects.get(id=shop_id)
#                 if cart:
#                     cart.delete()
#                 cart = Cart.objects.create(
#                     user=user, shop=shop, is_checkout=False)

#             cart_item = CartItem.objects.filter(
#                 cart=cart,
#                 product__id=product_id
#             ).first()

#             if cart_item is None:
#                 product = Product.objects.get(id=product_id)
#                 cart_item = CartItem.objects.create(
#                     cart=cart, product=product, quantity=quantity)
#             else:
#                 cart_item.quantity = quantity
#                 cart_item.save()

#             result = CartItemSerializer(cart_item, many=False).data
#             return Response(result, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 f"Unable to update cart item. {e}",
#                 status=status.HTTP_404_NOT_FOUND
#             )

class CartViewSet(viewsets.ModelViewSet):
    # queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if (self.request.user.is_staff):
            return Cart.objects.all()
        else:
            current_user = get_object_or_404(
                User, pk=self.request.user.id)

            current_customer = get_object_or_404(Customer, user=current_user)
            newest_cart = Cart.objects.filter(
                customer=current_customer).first()
            return newest_cart

    def get_permissions(self):
        if self.action in ['list']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SimpleCartSerializer
        if self.request.method == "POST":
            return CreateCartSerializer
        if self.action == "my_cart":
            return UpdateCartItemsSerializer
        return CartSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def my_cart(self, request, *args, **kwargs):
        print(self.request.method)
        newest_cart = self.get_queryset()
        if request.method in ['GET']:
            serializer = SimpleCartSerializer(newest_cart)
            return Response(serializer.data)
        if request.method in ['PUT']:
            cart_items_serializer = self.get_serializer(
                data=request.data)
            print('cart_items_serializer : ', cart_items_serializer)
            cart_items_serializer.is_valid(raise_exception=True)
            cart_items_serializer.save(cart_id=newest_cart.id)
            print('cart_items_serializer.data : ', cart_items_serializer.data)
            return Response(cart_items_serializer.data)
