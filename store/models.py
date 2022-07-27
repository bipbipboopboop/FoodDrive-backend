from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib import admin


ORDERS_RELATED_NAME = 'orders'
PRODUCTS_RELATED_NAME = 'products'
REVIEWS_RELATED_NAME = 'reviews'
OWNER_RELATED_NAME = 'owners'
CARTS_RELATED_NAME = 'carts'


class Shop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    image_link = models.TextField()
    # owner
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
    shop = models.OneToOneField(
        Shop, on_delete=models.SET_NULL, related_name=OWNER_RELATED_NAME, null=True)

    # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    # DO_NOTHING: Probably a very bad idea since this would create integrity issues in your database
    # (referencing an object that actually doesn't exist). SQL equivalent:

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


class Order(models.Model):
    ORDER_STATUS_PENDING = 'PENDING'
    ORDER_STATUS_COMPLETE = 'COMPLETE'
    ORDER_STATUS_FAILED = 'FAILED'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_FAILED, 'Failed'),
        (ORDER_STATUS_COMPLETE, 'Complete')
    ]

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    order_status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_PENDING)
    shop = models.ForeignKey(
        Shop, on_delete=models.DO_NOTHING, related_name=ORDERS_RELATED_NAME)
    customer = models.ForeignKey(
        Customer, related_name=ORDERS_RELATED_NAME, on_delete=models.DO_NOTHING)

    # order_items

    def __str__(self) -> str:
        return self.order_status


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    # ordered_items

    def __str__(self) -> str:
        return f'{self.order} - {self.product} - {self.quantity}'


class OrderHistory(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='order_history')
    # ordered_items

    def __str__(self) -> str:
        return f'{self.customer} - {self.id}'


class OrderHistoryItem(models.Model):
    history = models.ForeignKey(
        OrderHistory, on_delete=models.CASCADE, related_name='ordered_items')
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f'{self.history} - {self.order_item}'


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
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    customer = models.OneToOneField(
        Customer, related_name=CARTS_RELATED_NAME, on_delete=models.CASCADE, null=True)
    is_checkout = models.BooleanField(default=False)
    # cart_items

    def __str__(self):
        return f'{self.id} - {self.customer}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    # class Meta:
    #     unique_together = [['cart', 'product']]

    def __str__(self):
        return f'{self.cart} - {self.product}'
