from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer, OrderSerializer, OwnerSerializer, ProductSerializer, ReviewSerializer, ShopSerializer
from .models import Customer, Order, Owner, Product, Review, Shop

from pprint import pprint


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()

    def get_queryset(self):
        url_param = self.kwargs
        if ('shop_pk' in url_param):
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
        pprint(self.kwargs)
        pprint('shop_pk' in url_param)
        if ('product_pk' in url_param):
            return Review.objects.filter(product_id=self.kwargs['product_pk'])
        elif ('shop_pk' in url_param):
            return Review.objects.filter(shop_id=self.kwargs['shop_pk'])
        else:
            return None


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# We don't really need a list of customers


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
