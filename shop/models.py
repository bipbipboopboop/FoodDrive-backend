from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.utils import timezone

VENDOR = 'vendor'
CUSTOMER = 'customer'
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """Create user by email, name, password"""
        if not email:
            raise ValueError('User must have an email!')
        user = self.model(email=self.normalize_email(
            email), name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Create superuser by email, name, password"""
        user = self.create_user(email=email, name="Admin", password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    User_Type = (
        (VENDOR, 'vendor'),
        (CUSTOMER, 'cusomter'),
    )
    user_type = models.CharField(max_length=40,
                                 choices=User_Type,
                                 default=VENDOR
                                 )
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['name', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    # def __repr__(self):
    #     return f"{self.email!r}, {self.is_staff!r}, {self.is_active!r}, "


class Store(models.Model):
    name = models.CharField(max_length=255)


class Menu(models.Model):
    title = models.CharField(max_length=255)


class Promotion(models.Model):
    discount = models.DecimalField(max_digits=3, decimal_places=0)


class Products(models.Model):
    title = models.CharField(max_length=255)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
