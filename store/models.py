from django.db import models
from django.conf import settings
from django.contrib import admin


ORDERS_RELATED_NAME = 'orders'
PRODUCTS_RELATED_NAME = 'products'
REVIEWS_RELATED_NAME = 'reviews'
OWNERS_RELATED_NAME = 'owners'


class Shop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    image_link = models.TextField()
    # owners
    # products
    # orders
    # reviews

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name=PRODUCTS_RELATED_NAME, null=True, blank=True)
    slug = models.SlugField()
    image_link = models.TextField()
    # orders
    # reviews

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'PENDING'
    PAYMENT_STATUS_COMPLETE = 'COMPLETE'
    PAYMENT_STATUS_FAILED = 'FAILED'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
        (PAYMENT_STATUS_COMPLETE, 'Complete')
    ]
    products = models.ManyToManyField(
        Product, related_name=PRODUCTS_RELATED_NAME)

    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name=ORDERS_RELATED_NAME, null=True, blank=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # order_items

    def __str__(self) -> str:
        return self.payment_status


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.order} - {self.product} - {self.quantity}'


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    # reviews

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Owner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, on_delete=models.DO_NOTHING, related_name=OWNERS_RELATED_NAME)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Review(models.Model):
    # One-to-many relation, related_name means that in Product Model, there will be a field called reviews
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name=REVIEWS_RELATED_NAME, null=True, blank=True)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name=REVIEWS_RELATED_NAME, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name=REVIEWS_RELATED_NAME)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.user.first_name} - {self.description}'


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
