from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
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

    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)

    def __str__(self) -> str:
        return self.payment_status


class Review(models.Model):
    # One-to-many relation, related_name means that in Product Model, there will be a field called reviews
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
