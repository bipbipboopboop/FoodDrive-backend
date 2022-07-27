from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .serializers import CreateOrderSerializer, OrderHistorySerializer, OrderHistoryItemSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, OwnerCreateSerializer, OwnerSerializer, ProductSerializer, ReviewSerializer, ShopSerializer
from .models import Cart, Customer, OrderHistory, OrderHistoryItem, Order, OrderItem, Owner, Product, Review, Shop

from pprint import pprint


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def is_vendor(self):
        return self.request.user.is_vendor

    def is_staff(self):
        return self.request.user.is_staff

    # def get_permissions(self):
    #     if (not self.is_vendor() and not self.is_staff()):
    #         return [IsAdminUser()]
    #     else:
    #         return [IsAuthenticated()]

    # def get_queryset(self):
    #     if (self.is_staff()):
    #         return Shop.objects.all()
    #     elif (self.is_vendor()):
    #         owner = Owner.objects.get(user=self.request.user)
    #         return Shop.objects.filter(owners=owner)
    #     else:
    #         return None

    @action(detail=False, methods=['GET', 'PUT'])
    def my_shop(self, request):
        owner = get_object_or_404(Owner, user_id=request.user.id)
        shop = get_object_or_404(Shop, owners=owner)

        if request.method == 'GET':
            serializer = ShopSerializer(shop)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ShopSerializer(
                shop, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):

    """
    Does not have permission yet :(
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        url_param = self.kwargs
        if ('shop_pk' in url_param):
            if (url_param['shop_pk'] == 'my_shop'):
                owner = get_object_or_404(Owner, user_id=self.request.user.id)
                shop = get_object_or_404(Shop, owners=owner)
                return shop.products
            else:
                return Product.objects.filter(shop_id=url_param['shop_pk'])
        else:
            return Product.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # Wanted to do queryset = Review.objects.filter(product_id = self.kwargs['product_id'])
    # However, self cannot be found
    # Hence, use get_queryset

    def get_queryset(self):
        url_param = self.kwargs

        if ('product_pk' in url_param):
            return Review.objects.filter(product_id=self.kwargs['product_pk'])
        elif ('shop_pk' in url_param):
            if (url_param['shop_pk'] == 'my_shop'):
                owner = get_object_or_404(Owner, user_id=self.request.user.id)
                shop = get_object_or_404(Shop, owners=owner)
                return shop.products.reviews
            else:
                return Review.objects.filter(shop_id=self.kwargs['shop_pk'])
        else:
            return None


class OwnerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Owner.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OwnerCreateSerializer
        return OwnerSerializer

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == "POST":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (current_owner, created) = Owner.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = OwnerSerializer(current_owner)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OwnerSerializer(
                current_owner, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # We don't really need a list of customers
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    # Available on list view /customers/me

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (current_customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(current_customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(
                current_customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Only Vendors or Staff can see orders
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if (self.request.user.is_staff):
            return Order.objects.all()
        if(self.request.user.is_vendor):
            current_owner = Owner.objects.get(user=self.request.user)
            shop = Shop.objects.get(owners=current_owner)
            return shop.orders

    def get_serializer_class(self):
        if (self.request.method == "POST"):
            return CreateOrderSerializer
        return OrderSerializer

    def get_my_cart(self):
        current_customer = get_object_or_404(Customer, user=self.request.user)
        (current_cart, created) = Cart.objects.get_or_create(
            customer=current_customer, is_checkout=False)

        return current_cart

    def get_serializer_context(self):
        if(self.request.user.is_vendor):
            return {}
        return {'cart': self.get_my_cart()}


class OrderHistoryViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        if (self.request.user.is_staff):
            return OrderHistory.objects.all()
        else:
            customer = get_object_or_404(Customer, user=self.request.user)
            return OrderHistory.objects.filter(customer=customer)


class OrderHistoryItemViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistoryItemSerializer

    def get_queryset(self):
        if (self.request.user.is_staff):
            return OrderHistoryItem.objects.all()
        else:
            customer = get_object_or_404(Customer, user=self.request.user)
            return OrderHistoryItem.objects.filter(customer=customer)
