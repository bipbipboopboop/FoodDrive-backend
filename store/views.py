from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ProductSerializer, ReviewSerializer
from .models import Product, Review


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
