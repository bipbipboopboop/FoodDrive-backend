from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = router.urls
