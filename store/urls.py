from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from store import cart_views
from . import views
from store.cart_views import CartViewSet


router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='Product')
router.register('owners', views.OwnerViewSet)
router.register('orders', views.OrderViewSet, basename='Order')
router.register('shops', views.ShopViewSet, basename='shops')
router.register('customers', views.CustomerViewSet, basename='customers')
# router.register('carts', views.CartViewSet)
router.register('carts', cart_views.CartViewSet, basename="Cart")

router.register('carts/my_cart/cart_items',
                cart_views.CartItemViewSet, basename="CartItem")


products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

# /store/shops/1/products
shops_router = routers.NestedDefaultRouter(
    router, 'shops', lookup='shop')
shops_router.register('products', views.ProductViewSet,
                      basename='shop-products')
shops_router.register('reviews', views.ReviewViewSet,
                      basename='shop-reviews')
shops_router.register('orders', views.OrderViewSet,
                      basename='shop-orders')

# /store/shops/1/products/1/review


orders_router = routers.NestedDefaultRouter(
    shops_router, 'orders', lookup='order')
orders_router.register('products', views.ProductViewSet,
                       basename='order-products')


urlpatterns = router.urls + products_router.urls + \
    shops_router.urls + orders_router.urls
