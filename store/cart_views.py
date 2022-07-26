
from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from store.models import Cart, CartItem, Customer
from store.cart_serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, SimpleCartSerializer, MyCartSerializer


class CartViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'destroy']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        if (self.request.user.is_staff):
            return Cart.objects.all()
        else:
            # Check if you are a customer, if you are not, raise an error
            current_customer = get_object_or_404(
                Customer, user=self.request.user)
            return Cart.objects.filter(customer=current_customer)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SimpleCartSerializer
        if self.action == "my_cart":
            return MyCartSerializer
        return CartSerializer

    @action(detail=False, methods=['GET'])
    def my_cart(self, request, *args, **kwargs):
        print(self.request.method)
        current_customer = get_object_or_404(Customer, user=request.user)
        newest_cart = Cart.objects.filter(
            customer=current_customer, is_checkout=False).first()
        if newest_cart is None:
            newest_cart = Cart.objects.create(customer=current_customer)

        if request.method in ['GET']:
            serializer = self.get_serializer(instance=newest_cart)
            return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_my_cart(self):
        current_customer = get_object_or_404(Customer, user=self.request.user)
        (current_cart, created) = Cart.objects.get_or_create(
            customer=current_customer, is_checkout=False)
        return (current_cart, created)

    def get_queryset(self):
        (current_cart, created) = self.get_my_cart()
        if not created:
            return current_cart.cart_items
        else:
            return CartItem.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart': self.get_my_cart()[0]}


"""
Cart
    -cart_items
    -customer
    -is_checkout
Order
    -order_items
    -shop
    -customer
    -order_status

CartViewSet:
    -list(only admin)
    -retrieve(only admin)
    -update(only admin)
    -delete(only admin)

    -create(everyone)
        When current_customer's latest cart is None

    -my_cart(only customer can see their own cart)
        -GET: Show latest cart of a customer
        -PATCH: Update the cart_items of a customer
    
"""
