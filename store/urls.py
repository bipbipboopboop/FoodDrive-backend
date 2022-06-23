from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('owners', views.OwnerViewSet)
router.register('orders', views.OrderViewSet)
router.register('shops', views.ShopViewSet)


products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

shops_router = routers.NestedDefaultRouter(
    router, 'shops', lookup='shop')
shops_router.register('reviews', views.ReviewViewSet,
                      basename='shop-reviews')
shops_router.register('orders', views.OrderViewSet,
                      basename='shop-orders')


orders_router = routers.NestedDefaultRouter(
    shops_router, 'orders', lookup='order')
orders_router.register('products', views.ProductViewSet,
                       basename='order-products')


urlpatterns = router.urls + products_router.urls + \
    shops_router.urls + orders_router.urls
