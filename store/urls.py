
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from store import cart_views
from . import views


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
router.register('order_history', views.OrderHistoryViewSet,
                basename="order_history")

order_history_router = routers.NestedDefaultRouter(
    router, 'order_history', lookup='order_history')
order_history_router.register(
    'ordered_items', views.OrderHistoryItemViewSet, basename='ordered_history-items')

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


shop_orders_router = routers.NestedDefaultRouter(
    shops_router, 'orders', lookup='orders')
shop_orders_router.register('order_items', views.OrderItemViewSet,
                            basename='order-order_items')


urlpatterns = router.urls + products_router.urls + \
    shops_router.urls + shop_orders_router.urls
