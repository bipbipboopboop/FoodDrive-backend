from store.models import Cart, Customer
from store.views import OrderViewSet
from .serializers import CreatePaymentSerializer
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
import environ

env = environ.Env()
stripe.api_key = env('STRIPE_SECRET_KEY')

# Create your views here.


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


class CreatePaymentView(APIView):

    def post(self, request, *args, **kwargs):
        current_customer = get_object_or_404(Customer, user=request.user)
        my_cart = get_object_or_404(Cart, customer=current_customer)
        my_cart_items = my_cart.cart_items.all()

        serializer = CreatePaymentSerializer(
            data={},
            many=False,
            context={"cart_items": my_cart_items},
        )

        serializer.is_valid()
        data = serializer.data
        if not data:
            return Response(data={"error": "Cart items can't be empty!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = stripe.checkout.Session.create(**data)
            OrderViewSet.as_view({"post": "create"})(request._request)
            return Response(data={"url": response.url}, status=status.HTTP_200_OK)
