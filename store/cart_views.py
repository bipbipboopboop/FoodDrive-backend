
from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from main.models import User

from store.models import Cart, Customer
from store.cart_serializers import CartSerializer, SimpleCartSerializer, CreateCartSerializer, UpdateCartItemsSerializer


class CartViewSet(viewsets.ModelViewSet):
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
