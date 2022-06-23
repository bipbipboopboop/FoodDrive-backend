from django.contrib import admin
from store.models import Customer, Owner, Product, Review, Shop
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Owner)
admin.site.register(Shop)
