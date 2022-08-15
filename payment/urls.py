from django.urls import path
from payment import views

urlpatterns = [
    path('test-payment/', views.test_payment),
    path('create-payment/', views.CreatePaymentView.as_view())
]
