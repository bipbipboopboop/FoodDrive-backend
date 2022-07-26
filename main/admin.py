from django.contrib import admin
from store.models import Cart, CartItem, Customer, Order, OrderItem, Owner, Product, Review, Shop
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name",
         "last_name", "email", "is_vendor")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_vendor'),
        }),
    )


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Owner)
admin.site.register(Shop)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
